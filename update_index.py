from __future__ import annotations
from datetime import date

import json
import argparse


def get_input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', required=True, type=str, help='Package object JSON input string.')
    parser.add_argument('--index-file', required=True, type=str, default='index.json', help='Packages Downloads index file.')
    parser.add_argument('--release-date', type=str, default=date.today().isoformat(), help='Package release date.')
    parser.add_argument('--url', type=str, help='Package download URL.')
    parser.add_argument('--reference-url', type=str, help='Package reference download URL.')

    return parser.parse_args()


def get_or_create_object(parent_object: list[dict], key: str, value: str, default_object: dict) -> dict:
    try:
        existing_object = next(obj for obj in parent_object if obj[key] == value)
        print(f'"{key}": "{value}" already exists.')
        return existing_object
    except StopIteration:
        print(f'"{key}": "{value}" doesn\'t exist. Adding it ...')
        new_object = default_object.copy()
        new_object[key] = value
        parent_object.append(new_object)
        return new_object


def load_json(file: str) -> list[dict]:
    with open(file, 'r') as f:
        return json.load(f)


def write_json(file: str, data: list[dict]) -> None:
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)


def main() -> None:
    args = get_input_args()

    package_input = json.loads(args.package)

    index = load_json(args.index_file)

    area_object = {
        'area': package_input['healthAreaName'],
        'code': package_input['healthAreaCode'],
        'packages': []
    }
    area = get_or_create_object(index['areas'], 'area', package_input['healthAreaName'], area_object)

    package_object = {
        'name': package_input['description'],
        'code': package_input['code'],
        'packageVersions': []
    }
    package = get_or_create_object(area['packages'], 'code', package_input['code'], package_object)

    package_version_object = {
        'version': package_input['version'],
        'releaseDate': args.release_date,
        'translations': []
    }
    package_version = get_or_create_object(package['packageVersions'], 'version', package_input['version'], package_version_object)

    translation_language_object = {
        'language': package_input['locale'],
        'dhis2Versions': []
    }
    translation_language = get_or_create_object(package_version['translations'], 'language', package_input['locale'], translation_language_object)

    default_url_pattern = f"https://packages.dhis2.org/{package_input['locale']}/{package_input['code']}/{package_input['version']}/{package_input['DHIS2Version']}/"
    default_package_name_pattern = f"{package_input['code']}_{package_input['version']}_{package_input['DHIS2Version']}"
    default_reference_name_pattern = f"{package_input['code']}_COMPLETE_{package_input['version']}_{package_input['DHIS2Version']}"

    dhis2_version_object = {
        'version': package_input['DHIS2Version'],
        'metadataReference': args.reference_url if args.reference_url is not None else default_url_pattern + default_reference_name_pattern + '.xlsx',
        'url': args.url if args.url is not None else default_url_pattern + default_package_name_pattern + '.zip'
    }
    get_or_create_object(translation_language['dhis2Versions'], 'version', package_input['DHIS2Version'], dhis2_version_object)

    write_json(args.index_file, index)


if __name__ == '__main__':
    exit(main())
