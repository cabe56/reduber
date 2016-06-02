#!/bin/bash
env $(cat .env | xargs) python server.py
