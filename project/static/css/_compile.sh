#!/bin/bash

# apt-get install npm
# npm install -g less
# npm install -g less-plugin-clean-css

cd _less/
echo
echo ... Compiling
#lessc --compress semantic.less > ../semantic.min.css
lessc semantic.less --clean-css="--s1 --advanced --compatibility=ie8" > ../semantic.min.css
echo ... Done