"""
Remove *_unvalidated from granule file name.
"""
import re
import os
import boto3
from cumulus_logger import CumulusLogger
from cumulus_process import Process


logger = CumulusLogger('file_rename')


def replace_last_occurrence(raw_str, from_substr, repl_substr,
                            is_ignore_case=False):
    """
    This function replace the last occurance of the substring (from_substr)
    to a new substr (repl_substr) from the raw string
    :param raw_str:  the original string
    :param from_substr: the substring to be replace
    :param repl_substr: the substring to be replaced to
    :param is_ignore_case: True: ignore the case when searching the from_substr
    :return:
    """
    if is_ignore_case:
        index = raw_str.lower().rfind(from_substr.lower())
    else:
        index = raw_str.rfind(from_substr)  # index of the last occurrence of the substring
    return raw_str[:index] + repl_substr + raw_str[index + len(from_substr):]


class FileRename(Process):
    """
    Remove *_unvalidated from payload granule file objects
    rename *_unvalidated to * on s3
    """
    class_name = 'cumulusFileRename'
    str_replace_to_empty = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.logger.debug('{} Entered __init__', self.class_name)

    def replace_prevalidate(self, file):
        """
        replace the member variable str_replace_to_empty to empty string
        :param file: file object to process
        :return: new file object
        """
        file['fileName'] = replace_last_occurrence(file['fileName'], self.str_replace_to_empty,
                                                   '', True)
        file['key'] = replace_last_occurrence(file['key'], self.str_replace_to_empty,
                                              '', True)
        return file

    def replace_preset_str_2_empty(self, in_str):
        '''
        replaced the passed in string to empty
        :param in_str:
        :return:
        '''
        return re.sub(self.str_replace_to_empty, '', in_str, flags=re.IGNORECASE)

    def rename_file_on_s3(self, file):
        """
        rename a file on s3
        :param file: fileObject to be renamed
        :return:
        """
        s3_resource = boto3.resource('s3')
        s3_client = boto3.client('s3')
        bucket = file['bucket']
        source_key = file['key']
        # path = sourceKey.replace(file['fileName'], '')
        path = replace_last_occurrence(source_key, file['fileName'], '')
        destination_key = os.path.join(path, self.replace_preset_str_2_empty(file['fileName']))
        copy_source = {'Bucket': bucket, 'Key': source_key}
        self.logger.info(f'{self.class_name} Trying to make a copy. bucket:{bucket} ' +
                         f'source:{source_key} destination:{destination_key}')
        s3_resource.meta.client.copy(CopySource=copy_source, Bucket=bucket,
                                     Key=destination_key)
        self.logger.info(f'{self.class_name} Successfully copy file. from filename: {source_key} ' +
                         f'to filename: {destination_key} ')
        s3_client.delete_object(Bucket=file['bucket'], Key=source_key)
        self.logger.info(f'{self.class_name} Successfully deleting file: {source_key}')

    def process(self):
        '''
        main process function
        :return:
        '''
        try:
            self.str_replace_to_empty = self.config['replaceToEmpty']
            self.logger.info(f'{self.class_name} String to be replaced to empty: ' +
                             f'{self.str_replace_to_empty}')
            final_output = {}
            output_files = []
            granules = self.input['granules']
            for granule in granules:
                files = granule['files']
                for file in files:
                    self.logger.info(f"{self.class_name} About to rename file: {file['fileName']}")
                    self.rename_file_on_s3(file)
                    new_file = self.replace_prevalidate(file)
                    output_files.append(new_file)

            final_output['output_files'] = output_files
            final_output['output_granules'] = granules

            self.logger.debug(
                f"{self.class_name} finished building up output message ")
        except Exception as exp:
            self.logger.error(f'{self.class_name} Exception during processing', exe_info=True)
            raise exp
        return final_output


def handler(event, context):
    '''
    lambda entry point
    :param event:
    :param context:
    :return:
    '''
    logger.setMetadata(event, context)
    return FileRename.cumulus_handler(event, context=context)
