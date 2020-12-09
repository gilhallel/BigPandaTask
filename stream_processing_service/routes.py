import json
from flask import Response
from stream_processing_service import app
from stream_processing_service import data_utils


@app.route('/events/<event_type>')
def eventsByType(event_type):
    event_counts = data_utils.counters.get_events_count()
    word_counts = data_utils.counters.get_words_of_event(event_type)

    return Response(json.dumps({ "count": event_counts[event_type], "words": word_counts }), mimetype='application/json')

@app.route('/events')
def events():
    event_counts = data_utils.counters.get_events_count()
    word_counts = data_utils.counters.get_words_count()

    return Response(json.dumps({ "events": event_counts, "words": word_counts }), mimetype='application/json')


@app.route('/last_min/events/<event_type>')
def LastMineventsByType(event_type):
    event_counts = data_utils.counters.get_last_min_events_count()
    word_counts = data_utils.counters.get_last_min_words_of_event(event_type)

    return Response(json.dumps({ "count": event_counts[event_type], "words": word_counts }), mimetype='application/json')


@app.route('/last_min/events')
def LastMinevents():
    event_counts = data_utils.counters.get_last_min_events_count()
    word_counts = data_utils.counters.get_last_min_words_count()

    return Response(json.dumps({ "events": event_counts, "words": word_counts }), mimetype='application/json')
