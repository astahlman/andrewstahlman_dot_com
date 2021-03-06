.PHONY: clean
clean:
	rm -rf build/

dockerfile := Dockerfile
docker-build:
	docker build -t latest -f $(dockerfile) .

docker-run:
	docker run latest

docker-enter:
	docker run --rm -it -v $(PWD):/root/website --entrypoint /bin/bash latest
