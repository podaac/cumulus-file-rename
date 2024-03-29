from cumulus_file_rename import __version__
from cumulus_file_rename.cumulus_file_rename import FileRename, replace_last_occurrence
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
                        "fileName": "Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2_prevalidated.nc",
                        "key": "/MERGED_TP_J1_OSTM_OST_CYCLES_V42/Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2_prevalidated.nc",
                        "source": "s3://my-internal/staging/Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2_prevalidated.nc",
                        "bucket": "my-cumulus-test-input-v2",
                        "size": 18793236,
                        "checksumType": "md5",
                        "type": "data"
                    },
                    {
                        "fileName": "Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2.nc_prevalidated.md5",
                        "key": "/MERGED_TP_J1_OSTM_OST_CYCLES_V42/Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2.nc_prevalidated.md5",
                        "source": "s3://my-internal/staging/Merged_TOPEX_Jason_OSTM_Jason-3_Cycle_001.V4_2.nc_prevalidated.md5",
                        "bucket": "my-cumulus-test-input-v2",
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
    FileRename.rename_file_on_s3 = MagicMock(return_value=True)
    process = FileRename(**event)
    output = process.process()
    assert output['output_files'][0]['fileName'].find('_prevalidated') == -1
    assert output['output_granules'][0]['files'][0]['fileName'].find(
        '_prevalidated') == -1

def test_replace_last_occurance():
    event = test_arguments
    context = {}
    process = FileRename(**event)
    # test last occurance is at the trailing
    output = replace_last_occurrence(
        'aabbccddaa', 'aa', 'mm')
    assert output == 'aabbccddmm'
    # test last occurance is at the middle
    output = replace_last_occurrence(
        'aabbccddaaee', 'aa', 'mm')
    assert output == 'aabbccddmmee'
    # test the ignore case
    output = replace_last_occurrence(
        'aabbccddAaee', 'aa', 'mm', True)
    assert output == 'aabbccddmmee'


def test_replace_prevalidate():
    event = test_arguments
    context = {}
    process = FileRename(**event)
    process.str_replace_to_empty = '_prevalidated'
    output = process.replace_prevalidate(
        test_arguments['input']['granules'][0]['files'][0])
    if 'fileName' in output:
        assert output['fileName'].find('_prevalidated') == -1
    assert output['key'].find('_prevalidated') == -1
    if 'source' in output:
        assert output['source'].find('_prevalidated') == -1


def test_replacePresetStringToEmpty():
    event = test_arguments
    process = FileRename(**event)
    process.str_replace_to_empty = '_prevalidated'
    output = process.replace_preset_str_2_empty('This is not_prevalidated')
    assert output.find('_prevalidated') == -1
