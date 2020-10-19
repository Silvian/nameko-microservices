#!/bin/bash

cd services/orders

sleep 2
nameko run services --broker amqp://guest:guest@rabbitmq

