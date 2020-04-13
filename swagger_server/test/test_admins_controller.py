# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase
import base64


class TestAdminsController(BaseTestCase):
    """AdminsController integration test stubs"""

    def _test_admin_change_fail_attempts(self):
        """Test case for admin_change_fail_attempts

        Admin Change Number of game fail attempts
        """
        query_string = [('num_fail_attempts', 6)]
        username = 'john'
        password = 'spider'
        response = self.client.open(
            '/hanan8885/Hangman/1.0.0/admin/change_fail_attempts',
            method='PUT',
            query_string=query_string,
            headers={
                'Authorization': 'Basic ' + base64.b64encode(
                    bytes(username + ":" + password, 'ascii')).decode('ascii')

            }
        )
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    import unittest
    unittest.main()
