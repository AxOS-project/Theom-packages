#!/usr/bin/env python3

import argparse
import urllib.request
import urllib.error
import json
import os
import subprocess
import sys

GITHUB_REPO = "AxOS-project/Theom"
ASSET_EXT = ".tar.zst"

def fetch_release_asset_url(repo, release_type, ext):
    if release_type == "latest":
        api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    else:
        api_url = f"https://api.github.com/repos/{repo}/releases/tags/{release_type}"

    with urllib.request.urlopen(api_url) as response:
        data = json.load(response)

    for asset in data.get("assets", []):
        if asset["name"].endswith(ext):
            return asset["browser_download_url"], asset["name"]

    raise RuntimeError(f"No asset ending with {ext} found in release '{release_type}'.")

def download_asset(url, filename, output_dir="."):
    dest_path = os.path.join(output_dir, filename)
    with urllib.request.urlopen(url) as response, open(dest_path, 'wb') as out_file:
        out_file.write(response.read())
    print(f"Downloaded: {dest_path}")

def get_theom_version():
    try:
        result = subprocess.run(["pacman", "-Q", "theom-core"], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(version)
    except subprocess.CalledProcessError:
        print("Theom is not installed.", file=sys.stderr)
        sys.exit(1)

def get_version():
    try:
        result = subprocess.run(["pacman", "-Q", "theom-dev-tools"], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(version)
    except subprocess.CalledProcessError:
        print("Some error occurred.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--download-latest", action="store_true", help="Download the latest release")
    parser.add_argument("-d", "--download", metavar="TAG", help="Download a specific release tag")
    parser.add_argument("-o", "--output-dir", default=".", help="Directory to download the file into")
    parser.add_argument("-g", "--get-theom-version", action="store_true", help="Print installed version of Theom")
    parser.add_argument("-V", "--version", action="store_true", help="Print installed version of Theom Developer Tools")
    args = parser.parse_args()

    try:
        if args.get_theom_version:
            get_theom_version()
            sys.exit(0)

        if args.version:
            get_version()
            sys.exit(0)

        if args.download_latest:
            release_type = "latest"
        elif args.download:
            release_type = args.download
        else:
            parser.print_help()
            sys.exit(1)

        url, filename = fetch_release_asset_url(GITHUB_REPO, release_type, ASSET_EXT)
        download_asset(url, filename, output_dir=args.output_dir)

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        print(f"Error: {e}")
