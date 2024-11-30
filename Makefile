IMAGE:=grinatom-hack

help:
	@echo "help - show this help"
	@echo "build - build docker image"
	@echo "test - run tests"
	@echo "lint - run lining"
	@echo "run - start applicaion"
	@echo "dev - start applicaion in dev mode with live reload"

# TODO: fix make dev

clean:
	@docker rmi -f ${IMAGE}

build:
	@docker build -t ${IMAGE} . --network=host

dev: build
	@echo 'Run dev fastapi server.'
	@docker run --rm -v $(PWD):/app \
		-p 0.0.0.0:8000:8000 \
		-it ${IMAGE} \
		fastapi dev ./src/app.py

run: build
	@docker run --rm -it -p 0.0.0.0:8000:8000 ${IMAGE} 

test: build
	@echo 'Run tests'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m pytest --disable-warnings -v
