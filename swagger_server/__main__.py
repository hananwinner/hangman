#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.controllers import word_db, backend
import threading
import time
from flask.logging import create_logger

# BACKEND_INST = None
#
#
# def set_backend(inst):
#     global BACKEND_INST
#     BACKEND_INST = inst
#
#
# def get_backend():
#     return BACKEND_INST

from swagger_server.controllers.backend import create_instance



class ExpireThread(threading.Thread):
    def __init__(self, api_inst):
        threading.Thread.__init__(self)
        self._api_inst = api_inst
        self._is_stopping = False

    def stop(self):
        self._is_stopping = True

    def run(self):
        while not self._is_stopping:
            time.sleep(30)
            self._api_inst.expire_games()



def main():
    word_db_inst = word_db.WordDatabase()
    word_db_inst.load("wordlist.txt")
    api_inst = create_instance(word_db_inst)
    expire_thread = ExpireThread(api_inst)
    expire_thread.start()
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.name = 'hangman'
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Hangman API'}, pythonic_params=True)
    # app.app.logger.info("juweh")
    # app.logger.info("BACKEND_INST:\n", BACKEND_INST)

    app.run(port=8080)
    expire_thread.stop()
    expire_thread.join(timeout=10)


if __name__ == '__main__':
    main()
