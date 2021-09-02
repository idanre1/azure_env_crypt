#!/bin/sh

echo "*** Exporting environment variables"
eval `python env_from_aes_file.py -f $1 -p $2`

