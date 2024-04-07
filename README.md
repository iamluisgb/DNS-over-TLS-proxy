# DNS to DNS-over-TLS proxy


## Requirements

Design and create a
simple DNS to DNS-over-TLS proxy that we could use to enable our application to query a
DNS-over-TLS server.

- Handle at least one DNS query, and give a result to the client.
- Work over TCP and talk to a DNS-over-TLS server that works over TCP (e.g: Cloudflare).

###  Bonus
- Allow multiple incoming requests at the same time
- Also handle UDP requests, while still querying tcp on the other side.
