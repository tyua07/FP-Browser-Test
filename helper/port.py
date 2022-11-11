import socket


class Port(object):
    def __init__(self):
        self.port = self.free_port()
        pass

    def free_port(self):
        """
        Determines a free port using sockets.
        """
        free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        free_socket.bind(('127.0.0.1', 0))
        free_socket.listen(5)
        port = free_socket.getsockname()[1]
        free_socket.close()
        return port

    def get_port(self):
        return self.port
