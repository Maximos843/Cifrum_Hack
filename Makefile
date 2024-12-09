IMAGE := grinatom-hack
APP_DIR := ./src
TEST_DIR := ./tests

# Targets
.PHONY: help clean build dev run test lint

help:
	@echo "Available targets:"
	@echo "  help - Show this help message"
	@echo "  clean - Remove the Docker image"
	@echo "  build - Build the Docker image"
	@echo "  dev - Start the application in development mode with live reload"
	@echo "  run - Start the application in production mode"
	@echo "  test - Run tests"
	@echo "  lint - Run linting"

clean:
	@echo "Removing Docker image..."
	@docker rmi -f ${IMAGE}

build:
	@echo "Building Docker image..."
	@docker build -t ${IMAGE} . --network=host

dev:
	@echo "Starting development server with live reload..."
	@docker run --rm -v $(PWD):/app \
		-p 0.0.0.0:8000:8000 \
		-it ${IMAGE} \
		uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
		
run:
	@echo "Starting production server..."
	@docker run --rm -it -p 0.0.0.0:8000:8000 ${IMAGE}

test:
	@echo "Running tests..."
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m pytest --disable-warnings -v ${TEST_DIR}

lint:
	@echo "Running linting..."
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		flake8 ${APP_DIR}