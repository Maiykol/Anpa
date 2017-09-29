class Client:

    def __init__(self, connection, addr):
        # defining connection-socket to the server and address
        self.connection = connection
        self.addr = addr

        self.ip = addr[0]
        self.port = addr[1]
