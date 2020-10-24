FROM ubuntu:20.04

COPY requirements.txt /app/requirements.txt

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python3" ]

CMD [ "fog.py" ]