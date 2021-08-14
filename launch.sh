#!/bin/bash

# Delete previous Docker image if any
docker stop twt-to-english
docker rm twt-to-english

# Build Docker image
docker build -t twt-to-english .

# Run Docker image
docker run --name twt-to-english twt-to-english