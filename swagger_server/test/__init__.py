import logging
import connexion
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_testing import TestCase
from swagger_server.encoder import JSONEncoder
from swagger_server.controllers import word_db, backend
from swagger_server.__main__ import set_backend
from swagger_server.__main__ import ExpireThread


class MockWordDB(object):
    def get_random_word(self):
        return 'hello'


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        # self._expire_thread = ExpireThread(api_inst)
        # self._expire_thread.start()


    def create_app(self):
        word_db_inst = MockWordDB()
        api_inst = backend.GamesApi(word_db_inst)
        set_backend(api_inst)
        self._expire_thread = ExpireThread(api_inst)
        self._expire_thread.start()
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        return app.app

    def tearDown(self) -> None:
        super().tearDown()
        self._expire_thread.stop()
        self._expire_thread.join(timeout=10)


