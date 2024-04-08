import socket
import ssl
import multiprocessing
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration parameters
TLS_SERVER = ('1.1.1.1', 853)
PROXY_ADDRESS = '0.0.0.0'
PROXY_PORT_TCP = 53
PROXY_PORT_UDP = 53
BUFFER_SIZE = 1024

def handle_dns_query(data):
    """Handles a DNS query over TLS"""
    try:
        # Create SSL context
        context = ssl.create_default_context()

        # Connect to the DNS-over-TLS server
        with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=TLS_SERVER[0]) as tls_socket:
            tls_socket.connect(TLS_SERVER)
            tls_socket.send(data)
            response = tls_socket.recv(BUFFER_SIZE)
            return response
    except Exception as e:
        logger.error(f"Error processing DNS query over TLS: {e}")
        return None

def handle_tcp(tcp_socket):
    """Handles TCP connections"""
    try:
        while True:
            client_socket, client_address = tcp_socket.accept()
            logger.info(f"Incoming TCP connection from {client_address}")

            data = client_socket.recv(BUFFER_SIZE)
            logger.info(f"Data received via TCP: {data}")

            response = handle_dns_query(data)
            if response:
                client_socket.send(response)
            
            client_socket.close()
    except Exception as e:
        logger.error(f"Error handling TCP connection: {e}")

def handle_udp(udp_socket):
    """Handles UDP requests"""
    try:
        while True:
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)
            logger.info(f"Incoming UDP request from {addr}")

            response = handle_dns_query(len(data).to_bytes(2, 'big') + data)
            if response:
                udp_socket.sendto(response[2:], addr)
    except Exception as e:
        logger.error(f"Error handling UDP request: {e}")

def start_dns_proxy():
    """Initializes the DNS proxy server"""
    try:
        # Create TCP socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((PROXY_ADDRESS, PROXY_PORT_TCP))
        tcp_socket.listen(1)
        logger.info(f"DNS proxy server listening on {PROXY_ADDRESS}:{PROXY_PORT_TCP} for TCP")

        # Create UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((PROXY_ADDRESS, PROXY_PORT_UDP))
        logger.info(f"DNS proxy server listening on {PROXY_ADDRESS}:{PROXY_PORT_UDP} for UDP")

        # Create processes for handling TCP and UDP connections
        tcp_process = multiprocessing.Process(target=handle_tcp, args=(tcp_socket,))
        udp_process = multiprocessing.Process(target=handle_udp, args=(udp_socket,))
        tcp_process.start()
        udp_process.start()
    except Exception as e:
        logger.error(f"Error starting DNS proxy server: {e}")

if __name__ == "__main__":
    start_dns_proxy()
