#!/bin/bash
sudo docker stop tip_container
sudo docker rm tip_container
sudo docker run -d --name tip_container tip
