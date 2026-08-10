import requests
import time
import sys

API = "https://pam-latitude-homeless-prince.trycloudflare.com"

def gpu(op, **params):
    try:
        r = requests.post(f"{API}/job", json={"op": op, **params}, timeout=10)
        jid = r.json()["job_id"]
        print(f"Job {jid} queued...")
        while True:
            time.sleep(0.3)
            r = requests.get(f"{API}/result/{jid}", timeout=10)
            d = r.json()
            if d.get("status") == "done":
                return d["result"]
            elif "error" in d:
                return d
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("=" * 50)
    print("🖥️  Starting GPU Tests from VPS...")
    print("=" * 50)
    sys.stdout.flush()

    tests = [
        ("Vector Add (10M)", "add", {"n": 10_000_000}),
        ("Matrix Mult (4096)", "matmul", {"size": 4096}),
        ("Matrix Mult (8192)", "matmul", {"size": 8192}),
    ]

    for idx, (label, op, params) in enumerate(tests, 1):
        print(f"\n[{idx}/{len(tests)}] {label}:")
        sys.stdout.flush()
        result = gpu(op, **params)
        if isinstance(result, dict) and "ms" in result:
            print(f"   ✅ Time: {result['ms']:.2f} ms")
        else:
            print(f"   ❌ Error: {result}")
        sys.stdout.flush()

    print("\n" + "=" * 50)
    print("✅ All tests attempted!")
    print("=" * 50)
