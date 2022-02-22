#!/bin/bash

uvicorn api_rhizome_dev.app.main:app --host=127.0.0.1 --port=${PORT:-8002} --reload --debug
