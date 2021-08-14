#!/bin/bash

# Delete previous Docker image if any
sudo docker stop twt-to-english
sudo docker rm twt-to-english

# Build Docker image
sudo docker build -t twt-to-english .

# Run Docker image
sudo docker run --privileged --name twt-to-english twt-to-english