FROM python:3.7.7-slim-buster

RUN echo 'Updating Ubuntu packages.'
RUN apt-get update
RUN apt install -y gcc
RUN apt install -y g++
RUN apt install -y build-essential
RUN apt install -y python3.7-dev
RUN apt install -y python-dev

RUN echo 'Installing Python packages.'
RUN pip install --upgrade pip
ADD requirements.txt /
RUN pip install -r /requirements.txt

RUN echo 'Adding notebooks and scripts directories and docker-entrypoint.sh.'
ADD notebooks/ /workspace/notebooks
ADD scripts/ /workspace/scripts
COPY ["forecasting_take_home_data.csv", "scripts/", "/"]
ADD docker-entrypoint.sh /workspace/docker-entrypoint.sh
RUN chmod +x /workspace/docker-entrypoint.sh


RUN echo 'Declaring workspace to be the working directory.'
WORKDIR /workspace

RUN echo 'Exposing port 8888.'
EXPOSE 8888

RUN echo 'Setting /workspace/docker-entrypoint.sh as the entrypoint.'
ENTRYPOINT ["/workspace/docker-entrypoint.sh"]
