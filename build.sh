#!/usr/bin/env bash
set -o errexit

# Upgrade essential tools
pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements.txt
