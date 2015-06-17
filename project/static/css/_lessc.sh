#!/bin/bash

# apt-get install npm
# npm install -g less

cd _less/
echo
echo ... Compiling
lessc --compress semantic.less > ../semantic.min.css
echo ... Done