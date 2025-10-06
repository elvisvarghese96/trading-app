#!/bin/bash
cd /Users/elvisvarghese/Documents/RestApi
source stockenv/bin/activate
python script.py >> ticker_fetch.log 2>&1