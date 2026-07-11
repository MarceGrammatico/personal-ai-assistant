#!/usr/bin/env python3
"""
Personal AI Assistant - Terminal Client

Usage:
    uv run python -m cli [--base-url http://localhost:8000]
"""

import argparse
import json
import sys

import httpx


def main():
    parser = argparse.ArgumentParser(description="Personal AI Assistant CLI")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Base URL of the API server",
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Disable streaming (get full response at once)",
    )
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    stream = not args.no_stream
    conversation_id = None

    # Check connection
    try:
        resp = httpx.get(f"{base_url}/health", timeout=5)
        resp.raise_for_status()
        health = resp.json()
        print(f"\033[32m✓ Connected to {health['service']} v{health['version']}\033[0m")
    except Exception as e:
        print(f"\033[31m✗ Cannot connect to {base_url}: {e}\033[0m")
        sys.exit(1)

    print(f"  Streaming: {'on' if stream else 'off'}")
    print("  Type 'exit' or Ctrl+C to quit. 'new' to start a new conversation.\n")

    while True:
        try:
            user_input = input("\033[36mYou:\033[0m ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\033[33mBye!\033[0m")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\033[33mBye!\033[0m")
            break

        if user_input.lower() == "new":
            conversation_id = None
            print("\033[33m--- New conversation ---\033[0m\n")
            continue

        body = {
            "message": user_input,
            "stream": stream,
        }

        if conversation_id:
            body["conversation_id"] = conversation_id

        try:
            if stream:
                conversation_id = handle_stream(base_url, body)
            else:
                conversation_id = handle_sync(base_url, body)
        except httpx.HTTPStatusError as e:
            try:
                error_data = e.response.json()
                msg = error_data.get("error", {}).get("message", str(e))
            except Exception:
                msg = str(e)
            print(f"\033[31mError: {msg}\033[0m\n")
        except Exception as e:
            print(f"\033[31mError: {e}\033[0m\n")


def handle_sync(base_url: str, body: dict) -> str | None:
    """Send message and get full response."""

    resp = httpx.post(
        f"{base_url}/chat",
        json=body,
        timeout=120,
    )
    resp.raise_for_status()

    data = resp.json()
    print(f"\033[33mAssistant:\033[0m {data['answer']}\n")

    return data.get("conversation_id")


def handle_stream(base_url: str, body: dict) -> str | None:
    """Send message and stream response."""

    conversation_id = None

    with httpx.stream(
        "POST",
        f"{base_url}/chat",
        json=body,
        timeout=120,
    ) as resp:
        resp.raise_for_status()

        print("\033[33mAssistant:\033[0m ", end="", flush=True)

        buffer = ""
        for chunk in resp.iter_text():
            buffer += chunk
            lines = buffer.split("\n")
            buffer = lines.pop()

            for line in lines:
                if not line.startswith("data: "):
                    continue

                data = json.loads(line[6:])

                if data["type"] == "content":
                    print(data["data"], end="", flush=True)
                elif data["type"] == "done":
                    conversation_id = data.get("conversation_id")
                elif data["type"] == "error":
                    print(f"\n\033[31mError: {data['data']}\033[0m")

        print("\n")

    return conversation_id


if __name__ == "__main__":
    main()
