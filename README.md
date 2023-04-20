## Metadata Packages Downloads index updater

Updates the Metadata Packages Downloads [index.json](https://github.com/dhis2-metadata/downloads-index/blob/master/index.json) file based on the `package` object of a metadata package file.

### Usage

```shell
python3 update_index.py --package '{
  "DHIS2Build": "0ed6717",
  "DHIS2Version": "2.39.0.1-SNAPSHOT",
  "healthArea": "Tuberculosis",
  "code": "TB_CS",
  "description": "TB Case Surveillance",
  "lastUpdated": "20230124T224138",
  "locale": "en",
  "name": "TB_CS_TRK_DHIS2.39.0.1-SNAPSHOT-en",
  "type": "TRK",
  "version": "2.0.0"
}' --url 'https://example.org/archive.zip'
```

```shell
python3 update_index.py --package "$(jq -r '.package' < $package_file)" --url 'https://example.org/archive.zip' 
```

### Tests

Install the development dependencies:
```shell
pip install -r requirements-dev.txt
```

Run the tests:
```shell
pytest
```
