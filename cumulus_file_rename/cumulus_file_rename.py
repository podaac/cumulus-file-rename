import re
import boto3
from cumulus_logger import CumulusLogger
from cumulus_process import Process
from run_cumulus_task import run_cumulus_task

logger = CumulusLogger('file_rename')


class FileRename(Process):
    className = 'cumulusFileRename'
    strReplaceToEmpty = ''

    def __init__(self, *args, **kwargs):
        super(FileRename, self).__init__(*args, **kwargs)
        self.logger = logger
        self.logger.debug('{} Entered __init__', self.className)

    def replace_prevalidate(self, file):
        file['name'] = re.sub(self.strReplaceToEmpty, '',
                              file.get('name'), flags=re.IGNORECASE)
        file['filename'] = re.sub(self.strReplaceToEmpty, '', file.get(
            'filename'), flags=re.IGNORECASE)
        return file

    def replacePresetStringToEmpty(self, str):
        return re.sub(self.strReplaceToEmpty, '', str, flags=re.IGNORECASE)

    def renameFileOnS3(self, file):
        s3Resource = boto3.resource('s3')
        s3Client = boto3.client('s3')
        bucket = file['bucket']
        sourceKey = '{}/{}'.format(file['fileStagingDir'], file['name'])
        destinationKey = '{}/{}'.format(file['fileStagingDir'],
                                        self.replacePresetStringToEmpty(file['name']))
        copy_source = {'Bucket': bucket, 'Key': sourceKey}
        self.logger.info('{} Trying to make a copy. bucket:{} source:{} destination:{}'.format(
            self.className, bucket, sourceKey, destinationKey))
        s3Resource.meta.client.copy(CopySource=copy_source, Bucket=bucket,
                                    Key=destinationKey)
        self.logger.info('{} Successfully copy file. from filename: {} to filename: {} '
                    .format(self.className, sourceKey, destinationKey))
        s3Client.delete_object(Bucket=file['bucket'], Key=sourceKey)
        self.logger.info('{} Successfully deleting file: {} '
                    .format(self.className, sourceKey))

    def process(self):
        try:
            self.strReplaceToEmpty = self.config['replaceToEmpty']
            self.logger.info('{} String to be replaced to empty: {}'.format(
                self.className, self.strReplaceToEmpty))
            final_output = {}
            output_files = []
            granules = self.input['granules']
            for granule in granules:
                files = granule['files']
                for file in files:
                    self.logger.info("{} About to rename file: {}".format(
                        self.className, file['name']))
                    self.renameFileOnS3(file)
                    new_file = self.replace_prevalidate(file)
                    output_files.append(new_file)

            final_output['output_files'] = output_files
            final_output['output_granules'] = granules

            self.logger.debug(
                "{} finished building up output message ".format(self.className))
        except Exception as e:
            self.logger.error('{} Exception during processing'.format(
                self.className), exe_info=True)
            raise e

        return final_output


def handler(event, context):
    logger.setMetadata(event, context)
    return FileRename.cumulus_handler(event, context=context)
