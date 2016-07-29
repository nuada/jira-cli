#!/bin/bash

openssl genrsa -out private_key.pem 2048
chmod 600 private_key.pem
openssl rsa -pubout -in private_key.pem -out public_key.pem
