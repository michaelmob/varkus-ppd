#!/bin/bash
cd "${0%/*}"
cd ../
source env/bin/activate
pip $@