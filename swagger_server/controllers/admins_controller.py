import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server import util

from swagger_server.controllers.backend import get_instance


def admin_change_fail_attempts(num_fail_attempts):  # noqa: E501
    """Admin Change Number of game fail attempts

    Change the number of fail attempts allowed globally to all new games after the change # noqa: E501

    :param num_fail_attempts: 
    :type num_fail_attempts: int

    :rtype: None
    """

    get_instance().set_max_attempts(num_fail_attempts)
