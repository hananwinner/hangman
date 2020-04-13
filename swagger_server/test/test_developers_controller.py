# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.game import Game  # noqa: E501
from swagger_server.test import BaseTestCase
import time
from swagger_server.controllers.backend import GAME_EXPIRATION_SECONDS

class TestDevelopersController(BaseTestCase):
    def test_expiry(self):
        status = self._create_new_game()
        game_id = status["game_id"]
        self._test_get_game(game_id, 200)
        time.sleep(5)
        self._test_get_game(game_id, 200)
        time.sleep(GAME_EXPIRATION_SECONDS+20)
        self._test_get_game(game_id, 404)

    def _test_cancel(self):
        status = self._create_new_game()
        game_id = status["game_id"]
        self._test_cancel_game(game_id, 204)
        self._test_cancel_game(game_id, 404)

        status = self._test_guess_letter(game_id, 't', 404)





    def _test_play(self):
        status = self._create_new_game()
        game_id = status["game_id"]
        self.assertTrue("result" not in status)
        self.assertEqual(status["guess_status"], '_____')
        self.assertEqual(len(status["missed"]), 0)

        # attempt 1
        status = self._test_guess_letter(game_id,'t')
        self.assertTrue("result" not in status)
        self.assertEqual(status["guess_status"], '_____')
        self.assertEqual(len(status["missed"]), 1)

        # attempt 2
        status = self._test_guess_letter(game_id,'h')
        self.assertTrue("result" not in status)
        self.assertEqual(status["guess_status"], 'h____')
        self.assertEqual(len(status["missed"]), 1)

        # attempt 3
        status = self._test_guess_letter(game_id,'o')
        self.assertTrue("result" not in status)
        self.assertEqual(status["guess_status"], 'h___o')
        self.assertEqual(len(status["missed"]), 1)

        # unsuccessful attempt
        status = self._test_guess_letter(game_id, 'o', 500)

        status = self._test_get_game(game_id)
        self.assertTrue("result" not in status)
        self.assertEqual(status["guess_status"], 'h___o')
        self.assertEqual(len(status["missed"]), 1)

        # unsuccessful attempt
        status = self._test_guess_letter(game_id, 't', 500)

        status = self._test_get_game(game_id)
        self.assertTrue("result" not in status)
        self.assertEqual(status["guess_status"], 'h___o')
        self.assertEqual(len(status["missed"]), 1)

        # attempt 4
        status = self._test_guess_letter(game_id, 'l')
        self.assertTrue("result" not in status)
        self.assertEqual(status["guess_status"], 'h_llo')
        self.assertEqual(len(status["missed"]), 1)

        # attempt 5
        status = self._test_guess_letter(game_id, 'i')
        self.assertTrue("result" not in status)
        self.assertEqual(status["guess_status"], 'h_llo')
        self.assertEqual(len(status["missed"]), 2)

        # attempt 6
        status = self._test_guess_letter(game_id, 'u')
        self.assertEqual(status["result"], "lost")
        self.assertEqual(status["guess_status"], 'h_llo')
        self.assertEqual(len(status["missed"]), 3)


    def _test_cancel_game(self, game_id, response_code=None):
        """Test case for cancel_game

        Cancel the game
        """
        if response_code is None:
            response_code = 200

        response = self.client.open(
            '/hanan8885/Hangman/1.0.0/game/{game_id}'.format(game_id=game_id),
            method='DELETE')
        self.assertEqual(response.status_code, response_code)

    def _test_get_game(self, game_id, response_code=None):
        """Test case for get_game

        Get Game Status
        """
        no_data = False
        if response_code is None:
            response_code = 200
        else:
            no_data = True
        response = self.client.open(
            '/hanan8885/Hangman/1.0.0/game/{game_id}'.format(game_id=game_id),
            method='GET')
        data = response.data.decode('utf-8')
        self.assertEqual(response.status_code, response_code, 'Response body is : ' + data)
        return None if no_data else json.loads(data)

    def _test_guess_letter(self, game_id, letter, response_code=None):
        """Test case for guess_letter

        Guess a letter
        """
        no_data = False
        if response_code is None:
            response_code = 200
        else:
            no_data = True
        query_string = [('letter', letter)]
        response = self.client.open(
            '/hanan8885/Hangman/1.0.0/game/{game_id}'.format(game_id=game_id),
            method='POST',
            query_string=query_string)
        data = response.data.decode('utf-8')
        self.assertEqual(response.status_code, response_code, 'Response body is : ' + data)
        return None if no_data else json.loads(data)

    def _create_new_game(self, response_code=None):
        no_data = False
        if response_code is None:
            response_code = 200
        else:
            no_data = True
        response = self.client.open(
            '/hanan8885/Hangman/1.0.0/game',
            method='POST')
        data = response.data.decode('utf-8')
        self.assertEqual(response.status_code, response_code, 'Response body is : ' + data)

        return None if no_data else json.loads(data)


if __name__ == '__main__':
    import unittest
    unittest.main()
