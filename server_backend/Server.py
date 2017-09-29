import socket
import threading

from server_backend.Client import Client


class Server:
    """Creates a server listening specified port"""

    def __init__(self, port, ip, host, max_requests):
        self.port = port
        self.host = host
        self.ip = ip

        self.clients = []   # clients that contacted the server

        # retrieve listening socket
        self.sock = self.__init_socket(max_requests)


    def serve_forever(self):
        """Accepts connections to the server in an infinite loop and opens a new thread for each connection"""
        while True:
            # accepting connection and creating as client
            connection, addr = self.sock.accept()
            new_client = Client(connection, addr)

            # connection is handled by threading
            c_thread = threading.Thread(target=self.__handle_connection, args=[new_client])
            c_thread.daemon = True
            c_thread.start()

            # appending a connection
            self.clients.append(new_client)

            print("Connected Clients: ", self.clients)
            print("Currently active connection-threads: ", threading.active_count() - 1)


    def send_str(self, str, client):
        """Sends a string to specified client by creating a new sending thread"""
        s_thread = threading.Thread(target=self.__send_str, args=[str, client])
        s_thread.daemon = True
        s_thread.start()


    def __init_socket(self, max_req):
        """Inits listening socket"""
        # setting up to listen to IP4 and TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))

        sock.listen(max_req)
        return sock


    def __handle_connection(self, client):
        """Listens to data from a client"""
        while True:
            data = client.connection.recv(1024)

            print(f"Data received from client-IP '{client.ip}' on client's port '{client.port}.\nDATA: {data}\n")

            # sending msg back to confirm connection
            self.send_str("Connection succesful!\n", client)

            # break out if no data was received and remove connection
            if not data:
                self.clients.remove(client)
                break


    def __send_str(self, str, client):
        """Sends a string to a client"""
        client.connection.send(bytes(str, "utf-8"))




if __name__ == "__main__":
    HOST = ""
    PORT = 8888

    # IP of System in Network, to find go 'System Preferences > Network > Advanced... > TCP/IP'
    IP = "192.168.178.107"

    server = Server(PORT, IP, HOST, 1)
    server.serve_forever()