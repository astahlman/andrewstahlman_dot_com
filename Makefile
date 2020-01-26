.PHONY: clean
clean:
	rm -rf build/

docker-build:
	docker build -t latest -f Dockerfile .

docker-run:
	docker run latest

docker-enter:
	docker run --rm -it -v $(PWD):/root/website --entrypoint /bin/bash latest
