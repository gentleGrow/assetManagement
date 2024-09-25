#!/bin/bash
sudo docker stop dividend_container
sudo docker rm dividend_container
sudo docker run -d --name dividend_container dividend
