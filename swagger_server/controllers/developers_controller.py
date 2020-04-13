import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.game import Game  # noqa: E501
from swagger_server import util
from swagger_server.controllers import backend
from swagger_server.controllers.backend import get_instance
import flask

from functools import wraps


def game_error_decorator(op):
    @wraps(op)
    def _ex_handler_block(*args, **kwargs):
        try:
            return op(*args, **kwargs)
        except backend.GameError as ex:
            if "not found" in str(ex):
                return flask.make_response("game not found", 404)
            else:
                return flask.make_response(str(ex), 400)
        except ValueError:
            return flask.make_response("incorrect output", 400)
        # other errors will not be caught and
        # create the default server error 500 behaviour

    return _ex_handler_block


@game_error_decorator
def cancel_game(game_id):  # noqa: E501
    """Cancel the game

    Cancel the game # noqa: E501

    :param game_id: game id
    :type game_id: str

    :rtype: None
    """

    return get_instance().cancel_game(game_id)


@game_error_decorator
def get_game(game_id):  # noqa: E501
    """Get Game Status

    Get the game status, a row of underscores and letters, and the letters that already missed  # noqa: E501

    :param game_id: game id
    :type game_id: str

    :rtype: Game
    """
    return get_instance().get_game(game_id)


@game_error_decorator
def guess_letter(game_id, letter):  # noqa: E501
    """Guess a letter

    Guess a letter in the game. if the game exists, returns the status of the game after the word. # noqa: E501

    :param game_id: game id
    :type game_id: str
    :param letter: 
    :type letter: str

    :rtype: Game
    """
    return get_instance().play(game_id, letter)


@game_error_decorator
def new_game():  # noqa: E501
    """Create New Game

    Create a new game. Returns the new game status, a row of underscores, and empty list for the letters that already missed  # noqa: E501


    :rtype: Game
    """
    return get_instance().create_new_game()
