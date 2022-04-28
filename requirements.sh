#!/bin/bash

which pacman &> /dev/null && { 
    sudo pacman -Syu docker
    systemctl start docker.service
    systemctl enable docker.service
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
    exit
}

which apt-get &> /dev/null && {
    sudo apt update
    sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release -y
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update

    sudo apt install docker-ce docker-ce-cli containerd.io -y
    sudo systemctl enable docker.service containerd.service
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
    exit
}