import socket
import ssl
import multiprocessing

# DNS-over-TLS server address and port (e.g., Cloudflare)
TLS_SERVER = ('1.1.1.1', 853)

# DNS server address and port
PROXY_ADDRESS = '0.0.0.0'
PROXY_PORT_TCP = 53
PROXY_PORT_UDP = 53

def handle_dns_query(data):
    # Create SSL context
    context = ssl.create_default_context()

    # Connect to DNS-over-TLS server
    with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=TLS_SERVER[0]) as tls_socket:
        tls_socket.connect(TLS_SERVER)
        tls_socket.send(data)

        # Receive response from DNS-over-TLS server
        response = tls_socket.recv(1024)
        return response

def handle_tcp(tcp_socket):
    while True:
        # Accept a connection
        client_socket, client_address = tcp_socket.accept()
        print(f"Connection from {client_address}")

        # Receive data
        data = client_socket.recv(1024)
        print(f"Received data: {data}")

        # Forward data to the DNS-over-TLS server
        response = handle_dns_query(data)

        # Forward response to the client
        client_socket.send(response)

        # Close the connection
        client_socket.close()

def handle_udp(udp_socket):
    while True:
        data, addr = udp_socket.recvfrom(1024)
        print(f"Received UDP request from {addr}")

        # Forward data to the DNS-over-TLS server
        response = handle_dns_query(len(data).to_bytes(2, 'big') + data)

        # Forward response to the client
        udp_socket.sendto(response[2:], addr)

def start_dns_proxy():
    # Create TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((PROXY_ADDRESS, PROXY_PORT_TCP))
    tcp_socket.listen(1)

    print(f"DNS proxy server listening on {PROXY_ADDRESS}:{PROXY_PORT_TCP} for TCP")

    # Create UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((PROXY_ADDRESS, PROXY_PORT_UDP))

    print(f"DNS proxy server listening on {PROXY_ADDRESS}:{PROXY_PORT_UDP} for UDP")

    # Create processes for handling TCP and UDP requests
    tcp_process = multiprocessing.Process(target=handle_tcp, args=(tcp_socket,))
    udp_process = multiprocessing.Process(target=handle_udp, args=(udp_socket,))
    tcp_process.start()
    udp_process.start()


if __name__ == "__main__":
    start_dns_proxy()
