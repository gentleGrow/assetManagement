#!/bin/bash
sudo docker stop realtime_stock_world_container
sudo docker rm realtime_stock_world_container
sudo docker run -d --name realtime_stock_world_container realtime_stock_world
