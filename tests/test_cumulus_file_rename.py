from cumulus_file_rename import __version__
from cumulus_file_rename.cumulus_file_rename import FileRename
from unittest.mock import MagicMock


test_arguments = {
    "cumulus_meta": {
        "execution_name": "357d5239-b4da-4867-8fba-c167ee32ba8b",
        "message_source": "sfn",
        "state_machine": "arn:aws:states:us-west-2:111111111111:stateMachine:fake-cumulus-IngestKinesis",
        "system_bucket": "fake-cumulus-internal",
        "workflow_start_time": 1593635510075,
        "queueName": "startSF"
    },
    "config": {
        "fileStagingDir": "testing/cumulus-py",
        "bucket": "cumulus-internal",
        "distribution_endpoint": "https://cumulus.com",
        "replaceToEmpty": "_prevalidated",
        "input_keys": {
            "input-1": "^.*-1.txt$",
            "input-2": "^.*-2.txt$",
            "from_config": True
        }
    },
    "input": {
        "granules": [
            {
                "granuleId": "20200101000000-JPL-L2P_GHRSST-SSTskin-MODIS_A-D-v02.0-fv01.0",
                "dataType": "MODIS_A-JPL-L2P-v2019.0",
                "sync_granule_duration": 3759,
                "files": [
                    {
                        "name": "Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2_prevalidated.nc",
                        "path": "MERGED_TP_J1_OSTM_OST_CYCLES_V42",
                        "filename": "s3://podaac-dev-cumulus-test-input-v2/MERGED_TP_J1_OSTM_OST_CYCLES_V42/Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2_prevalidated.nc",
                        "fileStagingDir": "file-staging/dyen-cumulus/MODIS_A-JPL-L2P-v2019.0___2019.0",
                        "bucket": "podaac-dev-cumulus-test-input-v2",
                        "size": 18793236,
                        "checksumType": "md5",
                        "type": "data"
                    },
                    {
                        "name": "Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2.nc_prevalidated.md5",
                        "path": "MERGED_TP_J1_OSTM_OST_CYCLES_V42",
                        "filename": "s3://podaac-dev-cumulus-test-input-v2/MERGED_TP_J1_OSTM_OST_CYCLES_V42/Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2.nc_prevalidated.md5",
                        "fileStagingDir": "file-staging/dyen-cumulus/MODIS_A-JPL-L2P-v2019.0___2019.0",
                        "bucket": "podaac-dev-cumulus-test-input-v2",
                        "size": 83,
                        "type": "metadata"
                    }
                ],
                "version": "2019.0"
            }
        ]
    }
}


def test_version():
    assert __version__ == '1.0.0'


def test_file_rename():
    event = test_arguments
    context = {}
    FileRename.renameFileOnS3 = MagicMock(return_value=True)
    process = FileRename(**event)
    output = process.process()
    assert output['output_files'][0]['name'].find('_prevalidated') == -1
    assert output['output_granules'][0]['files'][0]['name'].find(
        '_prevalidated') == -1


def test_replace_prevalidate():
    event = test_arguments
    context = {}
    process = FileRename(**event)
    output = process.replace_prevalidate(
        test_arguments['input']['granules'][0]['files'][0])
    assert output['name'].find('_prevalidated') == -1
    assert output['filename'].find('_prevalidated') == -1


def test_rreplacePresetStringToEmpty():
    event = test_arguments
    process = FileRename(**event)
    process.strReplaceToEmpty = '_prevalidated'
    output = process.replacePresetStringToEmpty('This is not_prevalidated')
    assert output.find('_prevalidated') == -1
