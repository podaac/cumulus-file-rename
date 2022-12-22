#!/bin/sh
rm -Rf venv build;mkdir venv

poetry export -f requirements.txt --output requirements.txt
pip3 install -r requirements.txt  --target ./venv
cp cumulus_file_rename/*.py ./venv
cd venv; zip -r ../artifact.zip .
