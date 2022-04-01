# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
