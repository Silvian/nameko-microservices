#!/bin/bash

cd services/alerts

sleep 2
nameko run services --broker amqp://guest:guest@rabbitmq
