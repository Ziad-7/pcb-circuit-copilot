import urllib.request
import time
import sys

print("[*] Connecting to FastAPI Backend (pre-warming ChromaDB)...")
for attempt in range(35):
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2) as r:
            if r.status == 200:
                print("[*] FastAPI Backend is fully online and ready!")
                sys.exit(0)
    except Exception:
        time.sleep(1)

print("[!] Warning: FastAPI took longer than 35s to start, launching frontend anyway...")
sys.exit(0)
