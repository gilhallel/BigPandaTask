import subprocess
from threading import Thread, RLock
import logging
import json
from pathlib import Path
import time
dirname = Path(__file__)
default_filename = dirname.parent / 'resources' / 'generator-windows-amd64.exe'

class Json_iterator:
    def __init__(self, cmd=default_filename):
        self.cmd = cmd
        self.json_ob = None

    def __iter__(self):
        p = subprocess.Popen(self.cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in iter(p.stdout.readline, ''):
            try:
                self.json_ob = json.loads(line[:-1])# removing new line from json incetance
                yield self.json_ob
            except ValueError as e:
                continue


class last_min_dictionery:
    def __init__(self):
        self.words_by_event_type_last_min = {}
        self.words_last_min = {}
        self.events_last_min = {}
        self.event_queue = []
        self.thread = Thread(target=self.last_sec, args=())
        self.thread.start()

    def last_sec(self):
        while(1):
            if self.event_queue:
                event = self.event_queue[0]
                if time.time() - event["timestamp"] > 60:
                    logging.info("removing event from 1 minute queue")
                    json_ob = self.event_queue.pop(0)
                    self.update_last_min_count(json_ob)
                else:
                    time.sleep(time.time() - event["timestamp"])
            else:
                time.sleep(1.0)

    def update_last_min_count(self, json_ob):
        #atomic operation are prortected therefor dictioneries can be updated
        self.events_last_min[json_ob['event_type']] -= 1
        self.words_last_min[json_ob['data']] -= 1
        self.words_by_event_type_last_min[json_ob['event_type']][json_ob['data']] -= 1


class Counters:
    def __init__(self):
        self.events = {}
        self.words = {}
        self.words_by_event_type = {}
        self.last_min_data = last_min_dictionery()

    def start(self):
        logging.info('starting generator thread')
        self.thread = Thread(target=self.iterate_stream, args=())
        self.thread.start()

    def count(self, json_ob):
        self.last_min_count(json_ob)
        self.overall_count(json_ob)

    def last_min_count(self, json_ob):
        #atomic operation are prortected therefor dictionery can be updated
        self.last_min_data.event_queue.append(json_ob)
        if json_ob['event_type'] in self.last_min_data.events_last_min:
            self.last_min_data.events_last_min[json_ob['event_type']] += 1
        else:
            self.last_min_data.events_last_min[json_ob['event_type']] = 1
            self.last_min_data.words_by_event_type_last_min[json_ob['event_type']] = {}

        if json_ob['data'] in self.last_min_data.words_last_min:
            self.last_min_data.words_last_min[json_ob['data']] += 1
        else:
            self.last_min_data.words_last_min[json_ob['data']] = 1

        if json_ob['data'] in self.last_min_data.words_by_event_type_last_min[json_ob['event_type']]:
            self.last_min_data.words_by_event_type_last_min[json_ob['event_type']][json_ob['data']] += 1
        else:
            self.last_min_data.words_by_event_type_last_min[json_ob['event_type']][json_ob['data']] = 1

    def overall_count(self, json_ob):

        if json_ob['event_type'] in self.events:
            self.events[json_ob['event_type']] += 1
        else:
            self.events[json_ob['event_type']] = 1
            self.words_by_event_type[json_ob['event_type']] = {}

        if json_ob['data'] in self.words:
            self.words[json_ob['data']] += 1
        else:
            self.words[json_ob['data']] = 1

        if json_ob['data'] in self.words_by_event_type[json_ob['event_type']]:
            self.words_by_event_type[json_ob['event_type']][json_ob['data']] += 1
        else:
            self.words_by_event_type[json_ob['event_type']][json_ob['data']] = 1


    def iterate_stream(self):
        json_iterator = Json_iterator()
        for j in json_iterator:
            self.count(j)

    # overall data
    def get_words_count(self):
        return self.words

    def get_events_count(self):
        return self.events

    def get_words_of_event(self, event_type):
        return self.words_by_event_type[event_type]

    # last minute data
    def get_last_min_words_count(self):
        return self.last_min_data.words_last_min

    def get_last_min_events_count(self):
        return self.last_min_data.events_last_min

    def get_last_min_words_of_event(self, event_type):
        return self.last_min_data.words_by_event_type_last_min[event_type]



global counters
counters = Counters()



