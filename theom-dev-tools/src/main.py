#!/usr/bin/env python3

import argparse
import urllib.request
import json
import os

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-latest", action="store_true", help="Download the latest release")
    parser.add_argument("--download", metavar="TAG", help="Download a specific release tag")
    parser.add_argument("--output-dir", default=".", help="Directory to download the file into")
    args = parser.parse_args()

    try:
        if args.install_latest:
            release_type = "latest"
        elif args.download:
            release_type = args.download
        else:
            raise ValueError("You must specify either --install-latest or --download <tag>")

        url, filename = fetch_release_asset_url(GITHUB_REPO, release_type, ASSET_EXT)
        download_asset(url, filename, output_dir=args.output_dir)

    except Exception as e:
        print(f"Error: {e}")
