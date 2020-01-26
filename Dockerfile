FROM alpine:latest
RUN apk update && apk add \
        bash \
        curl \
        emacs \
        git \
        python \
        perl \
        tree \
        file
RUN curl -fsSL https://raw.githubusercontent.com/cask/cask/master/go | python
WORKDIR /root/website
ADD entrypoint.sh project.org bootstrap-build.el Cask ./
ADD src ./src
ENTRYPOINT ["./entrypoint.sh"]
