#!/bin/bash

coverage run -m pytest

coverage xml

sonar-scanner
