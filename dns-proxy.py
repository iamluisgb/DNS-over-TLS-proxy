import socket
import ssl

# DNS-over-TLS server address and port (e.g., Cloudflare)
TLS_SERVER = ('1.1.1.1', 853)

# DNS server address and port
PROXY_ADDRESS = '0.0.0.0'
PROXY_PORT_TCP = 2003

def handle_tcp(tcp_socket):
    while True:
        # Accept a connection
        client_socket, client_address = tcp_socket.accept()
        print(f"Connection from {client_address}")

        # Receive data
        data = client_socket.recv(1024)
        print(f"Received data: {data}")

        # Create SSL context
        context = ssl.create_default_context()

        # Forward data to the DNS-over-TLS server
        with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=TLS_SERVER[0]) as tls_socket:
            tls_socket.connect(TLS_SERVER)
            tls_socket.send(data)

            # Receive data from the DNS-over-TLS server
            response = tls_socket.recv(1024)
            print(f"Received response: {response}")

            # Forward response to the client
            client_socket.send(response)

        # Close the connection
        client_socket.close()

def start_dns_proxy():
    # Create a TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((PROXY_ADDRESS, PROXY_PORT_TCP))
    tcp_socket.listen(1)

    print(f"DNS proxy server listening on {PROXY_ADDRESS}:{PROXY_PORT_TCP}")

    # Handle incoming connections
    while True:
        handle_tcp(tcp_socket)

if __name__ == "__main__":
    start_dns_proxy()
