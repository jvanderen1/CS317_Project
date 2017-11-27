import MySQLdb
from sshtunnel import SSHTunnelForwarder

# ssh variables
ssh_host = ('prclab.pr.erau.edu', 22)           # Port 22 is default for SSH . . .
ssh_user = 'vanderj3'
ssh_pass = 'Atitis00'
remote_bind_addr = ('pruxap04.erau.edu', 3306)  # Port 3306 is for MySQL . . .

# mysql variables
mysql_host = '127.0.0.1'                        # 'localhost' will not work for MySQL hostname . . .
mysql_user = 'vanderenj'
mysql_pass = 'Atitis00'


class SQLConnector(object):
    """Used to allow interaction with MySQL database

    Components:
        :param self.cursor: Allows SQL commands to be sent to MySQL database
        :param self.db: Holds information about currently connected database
        :param self.tunnel: Holds information about currently connected ssh
    """

    def __init__(self):
        """Initializes all necessary variables"""

        # Connect to SSH before connecting to database . . .
        self.tunnel = SSHTunnelForwarder(
            ssh_address_or_host=ssh_host,
            ssh_username=ssh_user,
            ssh_password=ssh_pass,
            remote_bind_address=remote_bind_addr
        )

        self.tunnel.start()

        # Connect to MySQL database . . .
        self.db = MySQLdb.connect(
            host=mysql_host,
            user=mysql_user,
            passwd=mysql_pass,
            port=self.tunnel.local_bind_port)

        # Cursor object for writing queries to db . . .
        self.cursor = self.db.cursor()

    # END def __init()__ #

    def close(self):
        """Closes connection to both database and ssh"""

        # Close connection to db . . .
        self.db.close()

        # Close connection to ssh . . .
        self.tunnel.close()

    # END def close() #
