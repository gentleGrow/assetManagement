#!/bin/bash
sudo docker stop realtime_stock_container
sudo docker rm realtime_stock_container
sudo docker run -d --name realtime_stock_container \
  -e PYTHONPATH=/app \
  realtime_stock
