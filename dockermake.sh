#!/bin/sh

docker build -t my-email-analyzer -f Dockerfile .

docker run -it -p 5000:5000 my-email-analyzer