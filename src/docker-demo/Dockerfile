# set base image (host OS)
# FROM python:3.8
FROM python:3.8-slim-buster

# update pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# set the working directory in the container
WORKDIR /

# copy the dependencies file to the working directory
COPY requirements.txt /

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . /

# Expose the prediction app through port 8501
EXPOSE 8501

# command to run on container start
CMD streamlit run predict.py

# Steps - execute the following to containerize the model
# If you are getting permission error while executing docker, just add sudo
# example - sudo docker build -t mushroomclassifier:latest .

# 1. To build the docker image
# sudo docker build -t mushroomclassifier:latest .

# 3. To list docker images
# sudo docker images

# 3. To run the prediction app from docker image
# sudo docker run -p 8501:8501 mushroomclassifier:latest

# Trouble Shooting dokcer
    # to list the container
    # docker container ls

    # stop the existing mushroomclassifier  container
    # docker stop 5418701b9236
    # docker rm -f 5418701b9236


    # To debug the docker image - optional
    # docker run -it mushroomclassifier bash

    # To delete all containers including its volumes and images
    # docker system prune -a
    # docker rm -vf $(docker ps -a -q)
    # docker rmi -f $(docker images -a -q)
    