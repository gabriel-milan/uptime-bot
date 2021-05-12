import socket


def is_up(ip: str, port: int):
    """Checks whether host is up"""

    # Configures a socket connection with TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Sets a timeout for connection attempt
    s.settimeout(5)

    # This will attempt to connect to the
    # specified server and port. If it fails,
    # an excepction will be raised
    try:
        # Attempt connection
        s.connect((ip, int(port)))
        # Close connection
        s.shutdown(2)
        # If code reaches here, host is up
        return True
    except:
        # If an exception is raised, host is
        # down
        return False
