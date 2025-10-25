#!/bin/bash

source .venv/bin/activate
exec uvicorn app.main:app --reload --host 0.0.0.0
