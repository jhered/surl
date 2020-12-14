FROM        ubuntu:18.04


RUN         apt-get update && apt-get install -y build-essential gnupg python3 python3-setuptools python3-pip
COPY        ./requirements.txt /app/requirements.txt
WORKDIR     /app

RUN         python3 -m pip install -r requirements.txt
COPY        acortador.py .

ENV         LC_ALL C.UTF-8
ENV         LANG C.UTF-8


EXPOSE      8080
ENTRYPOINT  ["python3"]
CMD         ["acortador.py"]