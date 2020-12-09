from stream_processing_service import data_utils
from flask import Flask
import logging
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


from stream_processing_service import routes

data_utils.counters.start()

if __name__ == '__main__':
    app.run(debug=True)
