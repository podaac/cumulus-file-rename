# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] 

### Added
### Changed
- **PODAAC-4360**
  - code change to be compliant with cumulus 11 message schema
  - move to public github and construct github action 
  - enhanced the code so while replacing string, not only targeting fileName, key and source
    but also consider that only key and bucket are required under new CMA message schema. 
    i.e. fileName and source could be missing.

### Deprecated
### Removed
### Fixed
### Security

## [v1.0.0] - 2020-08-31

### Added

- **PCESA-2247**
  - Implemented the FileRename functionality for Sentinel-6. 
  - After syncing granule to staging area (from provider s3 to internal bucket)
    - renaming the files on staging area by removing "_prevalidated" from file name
    - renaming all file name and url from the output message by removing "_prevalidated" word

### Changed
### Deprecated
### Removed
### Fixed
### Security
