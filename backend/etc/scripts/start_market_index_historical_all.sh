#!/bin/bash
sudo docker stop market_index_historical_all_container
sudo docker rm market_index_historical_all_container
sudo docker run -d --name market_index_historical_all_container market_index_historical_all