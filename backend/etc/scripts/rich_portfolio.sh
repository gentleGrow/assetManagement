#!/bin/bash
sudo docker stop rich_portfolio_container
sudo docker rm rich_portfolio_container
sudo docker run -d --name rich_portfolio_container rich_portfolio
