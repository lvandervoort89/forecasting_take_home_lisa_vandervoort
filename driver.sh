#!/bin/bash

set -euo pipefail

# This is the container tag.
CONTAINER_TAG=forecasting_take_home

COMMAND=${1:-}
if [[ -z "$COMMAND" ]]; then
  echo
  echo "COMMAND is empty!  Try help :)"
  echo "Exiting."
  exit 1
elif
    [[ $COMMAND != "docker-clean-unused" ]] &&
    [[ $COMMAND != "-c" ]] &&
    [[ $COMMAND != "--clean" ]] &&
    [[ $COMMAND != "docker-clean-all" ]] &&
    [[ $COMMAND != "build" ]] &&
    [[ $COMMAND != "-b" ]] &&
    [[ $COMMAND != "--build" ]] &&
    [[ $COMMAND != "jupyter" ]] &&
    [[ $COMMAND != "-j" ]] &&
    [[ $COMMAND != "--jupyter" ]] &&
    [[ $COMMAND != "stop" ]] &&
    [[ $COMMAND != "-s" ]] &&
    [[ $COMMAND != "--stop" ]] &&
    [[ $COMMAND != "python-modeling" ]] &&
    [[ $COMMAND != "-h" ]] &&
    [[ $COMMAND != "--hello" ]] &&
    [[ $COMMAND != "shell" ]] &&
    [[ $COMMAND != "-sh" ]] &&
    [[ $COMMAND != "--shell" ]]
then
  echo
  echo "Maybe you need some help:

The usage pattern is

bash driver.sh [COMMAND]

COMMANDS:
docker-clean-unused,-c,--clean:         Delete unused Docker containers.
docker-clean-all:                       Delete *ALL* Docker containers.
build,-b,--build:                       Build the Docker container.
test,-t,--test:                         Run tests.
jupyter,-j,--jupyter:                   Start the Jupyter server in the container.
stop,-s,--stop:                         Stop the container.
python-modeling,-pm,--pythonmodel:      Run scripts/python_model.py.
shell,-sh,--shell:                      Open a shell in the container."
  exit 1
fi

case $COMMAND in

docker-clean-unused | -c | --clean)

  echo
  echo "Deleting all unused Docker containers."
  docker system prune --all --force --volumes
  ;;

docker-clean-all)

  echo
  echo "Deleting *ALL* Docker containers, running or not!"
  docker container stop $(docker container ls --all --quiet) && docker system prune --all --force --volumes
  ;;

build | -b | --build)

  echo
  echo "Building the container and tagging it $CONTAINER_TAG."
  docker build --tag $CONTAINER_TAG .
  ;;

jupyter | -j | --jupyter)

  echo
  echo "Starting the Jupyter server."
  docker run \
    --publish 8888:8888 \
    --volume $(pwd)/notebooks:/workspace/notebooks \
    --detach $CONTAINER_TAG jupyter
  echo "Go to http://localhost:8888/."
  ;;

stop | -s | --stop)

  echo
  echo "Stopping the $CONTAINER_TAG container."
  docker container stop $(docker ps -q --filter ancestor=$CONTAINER_TAG)
  ;;

python-modeling | -pm | --pythonmodel)

  echo
  echo "Running scripts/python_analysis.py in the $CONTAINER_TAG container."
  docker run $CONTAINER_TAG python scripts/python_model.py
    ;;

shell | -sh | --shell)

  echo
  echo "Opening shell in $CONTAINER_TAG."
  docker run --interactive --tty \
    $CONTAINER_TAG /bin/sh
  ;;

esac
