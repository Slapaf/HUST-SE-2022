from init import *
import logging
import traceback

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except:
        logging.debug(traceback.print_exc(
            file=open(os.path.join(LOG_ROOT, 'traceback_INFO.txt'), 'w+')))
