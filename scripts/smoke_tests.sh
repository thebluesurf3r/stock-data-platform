#!/bin/bash

test -f models/stock_direction/v1/model.pkl
test -f models/stock_direction/v1/metadata.json

echo "Smoke tests passed"
