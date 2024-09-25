#!/bin/bash
sudo docker stop exchange_rate_container
sudo docker rm exchange_rate_container
sudo docker run -d --name exchange_rate_container exchange_rate
