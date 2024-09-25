DOCKERFILES_DIR=docker

CONTAINERS = realtime_stock_container stock_container realtime_index_world_container realtime_index_korea_container index_container dividend_container tip_container exchange_rate_container rich_portfolio_container
IMAGES = realtime_stock stock realtime_index_world realtime_index_korea index dividend tip exchange_rate rich_portfolio

SCRIPTS_DIR=etc/scripts
SHELL_SCRIPTS = realtime_stock.sh stock.sh realtime_index_world.sh realtime_index_korea.sh index.sh dividend.sh tip.sh exchange_rate.sh rich_portfolio.sh

all: stop_containers remove_containers remove_images build_images run_containers

stop_containers:
	@echo "Stopping containers..."
	$(foreach container, $(CONTAINERS), sudo docker stop $(container) || true &&) echo "Containers stopped."

remove_containers:
	@echo "Removing containers..."
	$(foreach container, $(CONTAINERS), sudo docker rm $(container) || true &&) echo "Containers removed."

remove_images:
	@echo "Removing images..."
	$(foreach image, $(IMAGES), sudo docker rmi $(image) || true &&) echo "Images removed."

build_images:
	@echo "Building images..."
	sudo docker build -t realtime_stock -f $(DOCKERFILES_DIR)/Dockerfile.realtime_stock .
	sudo docker build -t stock -f $(DOCKERFILES_DIR)/Dockerfile.stock .
	sudo docker build -t realtime_index_world -f $(DOCKERFILES_DIR)/Dockerfile.realtime_index_world .
	sudo docker build -t realtime_index_korea -f $(DOCKERFILES_DIR)/Dockerfile.realtime_index_korea .
	sudo docker build -t index -f $(DOCKERFILES_DIR)/Dockerfile.index .
	sudo docker build -t dividend -f $(DOCKERFILES_DIR)/Dockerfile.dividend .
	sudo docker build -t tip -f $(DOCKERFILES_DIR)/Dockerfile.tip .
	sudo docker build -t exchange_rate -f $(DOCKERFILES_DIR)/Dockerfile.exchange_rate .
	sudo docker build -t rich_portfolio -f $(DOCKERFILES_DIR)/Dockerfile.rich_portfolio .
	@echo "Images built."

run_containers:
	@echo "Running containers..."
	bash $(SCRIPTS_DIR)/realtime_stock.sh
	bash $(SCRIPTS_DIR)/stock.sh
	bash $(SCRIPTS_DIR)/realtime_index_world.sh
	bash $(SCRIPTS_DIR)/realtime_index_korea.sh
	bash $(SCRIPTS_DIR)/index.sh
	bash $(SCRIPTS_DIR)/dividend.sh
	bash $(SCRIPTS_DIR)/tip.sh
	bash $(SCRIPTS_DIR)/exchange_rate.sh
	bash $(SCRIPTS_DIR)/rich_portfolio.sh
	@echo "Containers are up and running."

stop: stop_containers
remove: remove_containers remove_images
build: build_images
run: run_containers
