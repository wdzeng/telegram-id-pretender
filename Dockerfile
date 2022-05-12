FROM python:3.10-alpine3.15
RUN pip3 install telethon
COPY main.py /app/main.py

WORKDIR /app
CMD python3 main.py

LABEL description="This script peeks at a telegram username and takes it over if avilable."
