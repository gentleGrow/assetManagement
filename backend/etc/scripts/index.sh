#!/bin/bash
sudo docker stop index_container
sudo docker rm index_container
sudo docker run -d --name index_container index
