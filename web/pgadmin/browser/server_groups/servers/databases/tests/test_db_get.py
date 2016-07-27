# #################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2016, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
# ##################################################################

from pgadmin.utils.route import BaseTestGenerator
from regression import test_utils as utils
from regression.test_setup import config_data
from regression.test_utils import get_ids


class DatabasesGetTestCase(BaseTestGenerator):
    """
    This class will fetch database added under last added server.
    """

    scenarios = [
        # Fetching default URL for database node.
        ('Check Databases Node URL', dict(url='/browser/database/obj/'))
    ]

    def setUp(self):
        """
        This function perform the three tasks
         1. Add the test server
         2. Connect to server

        :return: None
        """

        # Firstly, add the server
        utils.add_server(self.tester)
        # Secondly, connect to server/database
        utils.connect_server(self.tester)

    def runTest(self):
        """ This function will fetch added database. """

        all_id = get_ids()
        server_ids = all_id["sid"]

        db_ids_dict = all_id["did"][0]
        srv_grp = config_data['test_server_group']

        for server_id in server_ids:
            db_id = db_ids_dict[int(server_id)]
            db_con = utils.verify_database(self.tester, srv_grp, server_id,
                                           db_id)
            if db_con["info"] == "Database connected.":
                response = self.tester.get(
                    self.url + str(srv_grp) + '/' + str(server_id) + '/' +
                    str(db_id), follow_redirects=True)
                self.assertEquals(response.status_code, 200)

    def tearDown(self):
        """
        This function deletes the added database, added server
        and the 'parent_id.pkl' file which is created in setup() function.

        :return: None
        """

        utils.delete_database(self.tester)
        utils.delete_server(self.tester)
        utils.delete_parent_id_file()
