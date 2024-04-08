FROM python:3.9-slim

COPY dns-proxy.py /

CMD [ "python", "./dns-proxy.py" ]
