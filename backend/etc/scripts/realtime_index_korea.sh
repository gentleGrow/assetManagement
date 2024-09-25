#!/bin/bash
sudo docker stop realtime_index_korea_container
sudo docker rm realtime_index_korea_container
sudo docker run -d --name realtime_index_korea_container realtime_index_korea
