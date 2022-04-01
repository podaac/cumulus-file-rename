# FileRename

## How To Build

* docker build --rm --no-cache --tag file_rename:latest .
* docker run --rm -it -v <path for zip file>:/home/zip_file/ file_rename:latest

docker run --rm -it -v /User/me/develop/code_dir:/home/zip_file/ file_rename:latest

This packages a file rename lambda that rename files on the staging bucket as well as on output message
. This uses a docker and poetry to install all dependencies into a virtual environment. Then zips up all the dependencies into a .zip file to be deployed into an aws lambda.