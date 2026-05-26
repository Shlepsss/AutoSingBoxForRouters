import requests
import json

SUB_URL = "https://raw.githack.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt"

API_URL = "https://api.web2core.workers.dev"

def fetch_subscription():
    r = requests.get(SUB_URL, timeout=15)
    r.raise_for_status()
    return r.text

def filter_lines(raw: str):
    lines = raw.splitlines()
    clean = []

    for line in lines:
        if line.startswith(("vless://", "vmess://", "trojan://")):
            clean.append(line)

    return "\n".join(clean)

def build_config(clean_input: str):
    payload = {
        "core": "singbox",
        "input": "vless://4e783039-6260-4107-9a11-2ab7dc18ded8@185.242.19.251:80?encryption=none&type=ws&security=none&path=%2Fstatic&host=top2019950683.mwscdn.ru#%F0%9F%87%AB%F0%9F%87%AE%20Finland%20%5B%2ACIDR%5D",
        "options": {
            "addTun": True,
            "addSocks": True,
            "tunName": "singtun0",
            "genClashSecret": False,
            "useExtended": False,
            "detour": False
        }
    }

    r = requests.post(API_URL, json=payload, timeout=15)
    r.raise_for_status()

    return r.json()

def main():
    print("Downloading subscription...")
    raw = fetch_subscription()

    print("Filtering input...")
    clean = filter_lines(raw)

    if not clean:
        raise RuntimeError("No valid proxy lines found")

    print("Sending to API...")
    config = build_config(clean)

    print("Writing config.json...")
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("Done.")

if __name__ == "__main__":
    main()
