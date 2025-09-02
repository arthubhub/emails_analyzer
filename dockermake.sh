#!/bin/sh

docker build -t my-email-analyzer -f Dockerfile .

docker run -it my-email-analyzer
