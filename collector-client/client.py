import argparse
import json
import time
import urllib.request


def post_json(url: str, payload: dict[str, object]) -> None:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        response.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal collector client scaffold.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/api/v1")
    parser.add_argument("--collector-id", default="local-dev")
    parser.add_argument("--workspace-id", type=int, default=1)
    args = parser.parse_args()

    payload = {
        "workspace_id": args.workspace_id,
        "collector_id": args.collector_id,
        "collector_name": args.collector_id,
        "source_machine": "local",
        "client_version": "0.1.0",
        "online_status": "online",
        "last_heartbeat_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    post_json(f"{args.base_url}/collectors", payload)
    print("collector heartbeat sent")


if __name__ == "__main__":
    main()
