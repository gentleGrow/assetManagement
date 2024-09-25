#!/bin/bash
sudo docker stop stock_container
sudo docker rm stock_container
sudo docker run -d --name stock_container stock
