import requests
import json
import sys

SUB_URL = "https://raw.githack.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt"
API_URL = "https://api.web2core.workers.dev"

def fetch_subscription():
    r = requests.get(SUB_URL, timeout=15)
    status_code = r.status_code
    print(f"[HTTP STATUS] GET {SUB_URL} -> {status_code}")
    
    if status_code != 200:
        print(f"[ERROR RESPONSE] {r.text[:200]}")
    
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
        "input": clean_input,
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
    status_code = r.status_code
    print(f"[HTTP STATUS] POST {API_URL} -> {status_code}")
    
    # Пробуем получить ответ (может быть JSON или текст)
    try:
        response_data = r.json()
        print(f"[RESPONSE TYPE] JSON")
        if "error" in response_data:
            print(f"[API ERROR] {response_data['error']}")
    except:
        response_data = r.text
        print(f"[RESPONSE TYPE] TEXT/HTML")
        print(f"[RESPONSE BODY] {response_data[:500]}")
    
    # raise_for_status после вывода статуса
    r.raise_for_status()
    
    return response_data if isinstance(response_data, dict) else {"raw": response_data}

def main():
    print("=" * 50)
    print("Downloading subscription...")
    print("=" * 50)
    
    try:
        raw = fetch_subscription()
        print(f"[INFO] Downloaded {len(raw)} bytes")
        
        print("\n" + "=" * 50)
        print("Filtering input...")
        print("=" * 50)
        
        clean = filter_lines(raw)
        
        if not clean:
            raise RuntimeError("No valid proxy lines found")
        
        lines_count = len(clean.splitlines())
        print(f"[INFO] Found {lines_count} valid proxy lines")
        print(f"[SAMPLE] First line: {clean.splitlines()[0][:100]}...")
        
        print("\n" + "=" * 50)
        print("Sending to API...")
        print("=" * 50)
        
        config = build_config(clean)
        
        print("\n" + "=" * 50)
        print("Writing config.json...")
        print("=" * 50)
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("[SUCCESS] Config saved to config.json")
        
    except requests.exceptions.HTTPError as e:
        print(f"\n[HTTP ERROR] {e}")
        if hasattr(e.response, 'text'):
            print(f"[ERROR BODY] {e.response.text[:500]}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
