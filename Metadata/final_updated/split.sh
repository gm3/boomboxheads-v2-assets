#!/bin/bash

jq -c '.[]' combined_final.json | split -l 1 -a 3 -d --additional-suffix='.json' - output
