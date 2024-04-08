# DNS over TLS Proxy Server

## Overview

This repository hosts a DNS over TLS proxy server implemented in Python. The proxy server is designed to encrypt DNS queries using TLS before forwarding them to a DNS-over-TLS server (e.g., Cloudflare). It's capable of handling both TCP and UDP connections and provides an additional layer of security and privacy for DNS communication.

## Table of Contents

1. [Architecture](#architecture)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Security Considerations](#security-considerations)
6. [Integration](#integration)
7. [Future Improvements](#future-improvements)


## Architecture

The DNS over TLS proxy server is implemented in Python, utilizing the socket and multiprocessing modules for handling TCP and UDP connections. It listens on port 53 for both TCP and UDP traffic, encrypts DNS queries using TLS, and forwards them to the specified DNS-over-TLS server. The responses are then decrypted and sent back to the client.

It was studied whether it was better to use the **socket** or **socketserver** library. It was decided to use the **socket** library because, being lower level, it offers more control over the network components, allows optimizing performance and handling edge cases more effectively.

It was also studied which is the best option to handle mutlipple requirements. **Multiprocessing**, **threads** and **asyncio** were studied. The chosen one was **multiprocessing** for several reasons:

- **Paralllelism**: Multiprocessing allows true parallelism by running multiple processes concurrently, leveraging multiple CPU cores if available. This can significantly improve performance, especially for CPU-bound tasks.

- **Isolation**: Each process in multiprocessing runs in its own memory space, providing better isolation and fault tolerance compared to threads, which share the same memory space. This reduces the risk of data corruption and improves stability.

- **Scalability**: Multiprocessing scales well across multiple CPU cores and can handle large workloads more efficiently. This makes it suitable for high-performance network applications like the DNS over TLS proxy server, where scalability is crucial.

**Note**: Increasing the backlog parameter in the tcp_socket.listen(backlog) call allows the TCP server to handle a larger number of pending connections before it begins rejecting new incoming connections. This is particularly useful for scaling the server to accommodate spikes in traffic, as it enables the server to maintain more connections concurrently waiting to be accepted. However, it's crucial to balance this with available system resources. Boosting the backlog value consumes memory and may strain CPU resources, potentially leading to performance degradation or connection loss if the system lacks the necessary resources. Thus, careful monitoring of system resource usage and adjusting the backlog value accordingly is essential to ensure optimal server performance without compromising system stability.

## Features

- **DNS Encryption**: Encrypts DNS queries using TLS for enhanced security and privacy.
- **Supports TCP and UDP**: Handles both TCP and UDP connections to accommodate different DNS communication methods.
- **Multiprocessing**: Utilizes multiprocessing for handling multiple connections concurrently, improving performance and scalability.
- **Robust Error Handling**: Implements robust exception handling and logging for error tracking and debugging purposes.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/iamluisgb/DNS-over-TLS-proxy.git
    ```

2. Navigate to the project directory:

    ```bash
    cd DNS-over-TLS-proxy
    ```

3. Build the Docker image:

    ```bash
    docker build -t dns-proxy
    ```

## Usage

To start the DNS over TLS proxy server, simply run the following command:

```bash
docker run -d --name dns-proxy --network=host dns-proxy
```

Now you can make some udp and tcp requests:

```bash
kdig @127.0.0.1 google.com +tcp


kdig @127.0.0.1 google.com
```

## Security Concerns

When deploying this proxy server in a production environment, consider the following security concerns:
- **Data Privacy**: Ensure that encrypted DNS queries are adequately protected to prevent eavesdropping or interception of sensitive information.
- **Authentication**: Verify the identity of the DNS-over-TLS server to prevent man-in-the-middle attacks.
- **Access Control**: Restrict access to the proxy server to authorized clients or networks to prevent unauthorized usage or attacks.
- **Logging**: Be cautious with logging sensitive information, such as DNS query content, to avoid exposing user data or violating privacy regulations.

## Integration

To integrate this solution into a distributed, microservices-oriented, and containerized architecture:
- Deploy the proxy server as a containerized service using Docker or Kubernetes.
- Use container orchestration tools to manage scalability, availability, and load balancing.
- Implement service discovery mechanisms to dynamically locate and communicate with the proxy server.
- Integrate with existing microservices architecture by routing DNS traffic through the proxy server to enforce security policies and privacy measures.

## Future Improvements

Some potential improvements to consider for the project:
- **DNS Caching**: Implement caching mechanisms to store DNS query responses locally, improving performance and reducing latency.
- **Rate Limiting**: Introduce rate limiting to prevent abuse or denial-of-service attacks.
- **Configuration Options**: Provide configuration options for specifying DNS-over-TLS server, listening ports, and other parameters.
- **Monitoring and Metrics**: Add monitoring and metrics collection to track server performance, usage patterns, and potential security incidents.



