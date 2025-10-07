"""
get_socket.py
-------------
To create a socket, use the ``get_socket.init()`` function:
   
Example::
        >>> import get_socket
        >>> s = get_socket.init(80, muted=False)

Refer to:
  https://docs.micropython.org/en/latest/library/socket.html
"""
import socket

def init(port=80, muted=False):
    """Initialize a socket connection object

    :param port: Optional port (80 is the default)
    :type port: port number or None
    :param muted: False (default)
    :type muted: bool
    
    :return: socket
    :rtype: socket object

    """
    # Define the socket address tuple, listening for
    #   connections on all available network interfaces
    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]  

    # Create a socket object
    s = socket.socket()  

    # Enable address reuse for restarts
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind server socket to IP address and port
    s.bind(addr)  

    # Listen for any incoming client connections
    s.listen(1)

    # Display the address the socket is listening on,
    #   if not muted
    if not muted:  
        print('listening on: {}'.format(addr))
    
    return s
    