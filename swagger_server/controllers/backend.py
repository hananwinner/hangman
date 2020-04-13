import threading
from swagger_server.controllers import word_db
import uuid
import time

BACKEND_INST = None


def create_instance(word_db):
    global BACKEND_INST
    BACKEND_INST = GamesApi(word_db)
    return BACKEND_INST


def get_instance():
    global BACKEND_INST
    return BACKEND_INST


class GameError(ValueError):
    def __init__(self, message):
        super().__init__(message)


class Game(object):
    def __init__(self, game_id, word, max_attempts):
        self._game_id = game_id
        self._word = word
        self._guess_status = ['_' for _ in range(len(self._word))]
        self._missed = []
        self._is_done = False
        self._max_attempts = max_attempts
        self._num_attempts = 0
        self._num_letter_remains = len(word)
        self._game_result_status = ""
        self._start_timestamp = time.time()

    def is_done(self):
        return self._is_done

    def _set_maker_win(self):
        self._is_done = True
        self._game_result_status = "lost"

    def _set_guesser_win(self):
        self._is_done = True
        self._game_result_status = "won"

    def gen_status(self, extra=None):
        status = {
            "game_id": self._game_id,
            "missed": self._missed,
            "guess_status": ''.join(self._guess_status)
        }
        if extra is not None:
            status.update(extra)
        if self._game_result_status != "":
            status["result"] = self._game_result_status
        return status

    def play(self, letter):
        hit = False
        if len(letter) != 1:
            raise ValueError("letter should be string in length 1")
        if self._is_done:
            raise GameError("game is done")
        if letter in self._guess_status or letter in self._missed:
            raise GameError("Already guessed")
        index = self._word.find(letter, 0)
        if index < 0:
            self._missed.append(letter)
        else:
            hit = True
            while index >= 0:
                self._num_letter_remains -= 1
                self._guess_status[index] = letter
                index = self._word.find(letter, index+1)

        self._num_attempts += 1

        if self._num_letter_remains == 0:
            self._set_guesser_win()
        else:
            if self._num_attempts >= self._max_attempts:
                self._set_maker_win()
        return self.gen_status({'guess_result': 'hit'if hit else 'miss'})


class GamesApi(object):
    def __init__(self, word_db, max_attempts=6, game_expiration_sec=300):
        self._word_db = word_db
        self._games_dict = {}
        self._lock = threading.Lock()
        self._max_attempts = max_attempts
        self._game_expiration_sec = game_expiration_sec

    def set_max_attempts(self, max_attempts):
        self._max_attempts = max_attempts

    @staticmethod
    def _create_game_id():
        return str(uuid.uuid4())

    def create_new_game(self):
        game_id = self._create_game_id()
        word = self._word_db.get_random_word()
        game = Game(game_id, word, self._max_attempts)
        with self._lock:
            while game_id in self._games_dict:
                game_id = self._create_game_id()
            self._games_dict[game_id] = game
        return game.gen_status()

    def play(self, game_id, letter):
        with self._lock:
            if game_id not in self._games_dict:
                raise GameError("game not found")
            else:
                game = self._games_dict[game_id]
                status = game.play(letter)
                if game.is_done():
                    del self._games_dict[game_id]
                return status

    def get_game(self, game_id):
        with self._lock:
            if game_id not in self._games_dict:
                raise GameError("game not found")
            else:
                game = self._games_dict[game_id]
                return game.gen_status()

    def cancel_game(self, game_id):
        with self._lock:
            if game_id not in self._games_dict:
                raise GameError("game not found")
            else:
                del self._games_dict[game_id]

    def expire_games(self):
        now = time.time()
        with self._lock:
            to_be_deleted = []
            for game_id, game in self._games_dict.items():
                game_start =  game._start_timestamp
                duration = now - game_start
                if duration > self._game_expiration_sec:
                    to_be_deleted.append(game_id)
            for game_id in to_be_deleted:
                del self._games_dict[game_id]
