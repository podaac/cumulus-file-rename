#!/bin/sh
rm -Rf package
poetry build
poetry run pip install -t package dist/*.whl
cd package; zip -r ../artifact.zip .