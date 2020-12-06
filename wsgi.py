import logging
from setup.db import db
from run import APP

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting db Creation")
    db.create(False)
    logging.info("DB creation script complete.\r\nStarting the server")
    APP.run(debug=True, host='0.0.0.0')