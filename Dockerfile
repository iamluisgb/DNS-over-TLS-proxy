FROM python:3.9-slim

COPY dns-proxy.py /

EXPOSE 53/tcp
EXPOSE 53/udp

CMD [ "python", "./dns-proxy.py" ]
