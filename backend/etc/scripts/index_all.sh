#!/bin/bash
sudo docker stop index_all_container
sudo docker rm index_all_container
sudo docker run -d --name index_all_container index_all
