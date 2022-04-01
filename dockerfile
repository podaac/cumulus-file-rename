FROM lambci/lambda:build-python3.7

#ENV AWS_DEFAULT_REGION us-east-1

WORKDIR /home/
RUN mkdir virtualenv
RUN mkdir zip_file
RUN mkdir zip_temp

RUN pip install poetry

#RUN poetry new cumulus_file_rename
RUN mkdir cumulus_file_rename
WORKDIR /home/cumulus-file-rename/

COPY . .

RUN poetry config virtualenvs.path /home/virtualenv
RUN poetry install --no-dev


# RUN cp /home/cumulus-file-rename/cumulus_file_rename/cumulus_file_rename.py /home/virtualenv/*/lib/*/site-packages/
RUN cp /home/cumulus-file-rename/cumulus_file_rename/cumulus_file_rename.py /home/virtualenv/*/lib/*/site-packages/

RUN chmod -R 775 /home/virtualenv/*/lib/*/site-packages/

RUN cp -R /home/virtualenv/*/lib/*/site-packages/* /home/zip_temp/ 

WORKDIR /home/zip_temp

RUN zip -r /home/fileRename.zip .

CMD ["python", "/home/cumulus-file-rename/copy_zip.py"]

ENTRYPOINT []
