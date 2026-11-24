"""Smoke test a deployed QueryDoctor instance.

Run:
    python scripts/smoke.py https://querydoctor.onrender.com
    python scripts/smoke.py https://querydoctor.onrender.com --expect-version <SHA>
"""

import argparse
import sys
import time

import httpx

DEFAULT_LIVE_URL = "https://prince28-dev01-querydoctor-main.onrender.com"


def smoke_test(base_url: str, expect_version: str | None = None, timeout: float = 300.0) -> None:
    base_url = (base_url or "").strip().rstrip("/")
    if not base_url or not base_url.startswith(("http://", "https://")):
        base_url = DEFAULT_LIVE_URL
    start_time = time.time()
    client = httpx.Client(timeout=10.0)

    # 1. Wait for expected version on /health if specified
    if expect_version:
        print(f"Waiting for version '{expect_version}' at {base_url}/health...")
        while True:
            try:
                r = client.get(f"{base_url}/health")
                if r.status_code == 200:
                    data = r.json()
                    version = data.get("version")
                    if version == expect_version:
                        print(f"ok /health -> 200, version {version}")
                        break
                    print(f"waiting: {base_url}/health -> 200 {version}")
                else:
                    print(f"waiting: {base_url}/health -> {r.status_code}")
            except Exception as e:
                print(f"waiting: connection error ({e})")

            if time.time() - start_time > timeout:
                sys.exit(f"FAIL: Timed out waiting for version '{expect_version}'")
            time.sleep(5)
    else:
        r = client.get(f"{base_url}/health")
        if r.status_code != 200:
            sys.exit(f"FAIL: /health returned {r.status_code}: {r.text}")
        data = r.json()
        print(f"ok /health -> 200, version {data.get('version')}")

    # 2. Check /ready
    r = client.get(f"{base_url}/ready")
    if r.status_code != 200:
        sys.exit(f"FAIL: /ready returned {r.status_code}: {r.text}")
    print(f"ok /ready -> 200 {r.json()}")

    # 3. Check /v1/documents?limit=1
    r = client.get(f"{base_url}/v1/documents?limit=1")
    if r.status_code != 200:
        sys.exit(f"FAIL: /v1/documents returned {r.status_code}: {r.text}")
    print("ok /v1/documents?limit=1 -> 200")
    print("Smoke test passed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test the live QueryDoctor URL")
    parser.add_argument(
        "url",
        nargs="?",
        default=DEFAULT_LIVE_URL,
        help="Base URL of the deployed app (defaults to https://prince28-dev01-querydoctor-main.onrender.com)",
    )
    parser.add_argument("--expect-version", help="Expected git commit SHA in /health")
    args = parser.parse_args()

    smoke_test(args.url, expect_version=args.expect_version)


if __name__ == "__main__":
    main()
