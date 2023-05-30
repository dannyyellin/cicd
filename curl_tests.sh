#!/bin/bash

RESPONSE_1=$(curl -s -w "%{http_code}" -o /dev/null https://example.com/endpoint1)
RESPONSE_2=$(curl -s -w "%{http_code}" -o /dev/null https://example.com/endpoint2)
RESPONSE_3=$(curl -s -w "%{http_code}" -o /dev/null https://example.com/endpoint3)
echo "Response 1: $RESPONSE_1"
echo "Response 2: $RESPONSE_2"
echo "Response 3: $RESPONSE_3"