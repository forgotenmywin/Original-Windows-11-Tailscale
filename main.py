import requests
import time

API = "https://pam-latitude-homeless-prince.trycloudflare.com"

def gpu(op, **params):
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

# تست
if __name__ == "__main__":
    print("Testing GPU from VPS...")
    
    print("\n1. Vector Add (10M):")
    r = gpu("add", n=10_000_000)
    print(f"   Time: {r['ms']:.2f}ms")
    
    print("\n2. Matrix Multiply (4096x4096):")
    r = gpu("matmul", size=4096)
    print(f"   Time: {r['ms']:.2f}ms")
    
    print("\n3. Matrix Multiply (8192x8192):")
    r = gpu("matmul", size=8192)
    print(f"   Time: {r['ms']:.2f}ms")
    
    print("\n✅ All done! GPU works from VPS!")
