import requests
import time
import sys
import os

# تنظیم UTF-8 برای ویندوز (جلوگیری از خطای Unicode)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

# آدرس API (در صورت نیاز تغییر دهید)
API = "https://pam-latitude-homeless-prince.trycloudflare.com"

def gpu(op, **params):
    """
    ارسال درخواست به API برای اجرای عملیات GPU
    op: نوع عملیات (مثلاً 'add' یا 'matmul')
    **params: پارامترهای عملیات (مثلاً n=10_000_000)
    """
    try:
        # ارسال درخواست برای شروع job
        r = requests.post(f"{API}/job", json={"op": op, **params}, timeout=10)
        jid = r.json()["job_id"]
        print(f"Job {jid} queued...")
        
        start_time = time.time()
        timeout = 30  # حداکثر ۳۰ ثانیه منتظر نتیجه بمان
        
        while True:
            # اگر زمان timeout تمام شد، خطا برگردان
            if time.time() - start_time > timeout:
                return {"error": "Job timeout (30s)"}
            
            time.sleep(0.3)  # هر ۳۰۰ میلی‌ثانیه یکبار چک کن
            r = requests.get(f"{API}/result/{jid}", timeout=10)
            d = r.json()
            
            if d.get("status") == "done":
                return d["result"]
            elif "error" in d:
                return d
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # ========== تنظیمات ==========
    LIFETIME = 60  # ۱ دقیقه (۶۰ ثانیه) - اینجا زمان کل اجرا را مشخص کنید
    # =============================
    
    start = time.time()
    
    print("=" * 50)
    print("Starting GPU Tests from VPS...")
    print("=" * 50)
    sys.stdout.flush()

    # لیست تست‌ها: (برچسب, نوع عملیات, پارامترها)
    tests = [
        ("Vector Add (10,000,000 elements)", "add", {"n": 10_000_000}),
        ("Matrix Multiply (4096x4096)", "matmul", {"size": 4096}),
        ("Matrix Multiply (8192x8192)", "matmul", {"size": 8192}),
    ]

    # اجرای تست‌ها
    for idx, (label, op, params) in enumerate(tests, 1):
        print(f"\n[{idx}/{len(tests)}] {label}:")
        sys.stdout.flush()
        
        result = gpu(op, **params)
        
        if isinstance(result, dict) and "ms" in result:
            print(f"   Time: {result['ms']:.2f} ms")
        else:
            print(f"   Error: {result}")
        sys.stdout.flush()

    print("\n" + "=" * 50)
    print("All tests attempted.")
    print("=" * 50)

    # ========== منتظر ماندن تا پایان زمان تعیین‌شده ==========
    elapsed = time.time() - start
    remain = LIFETIME - elapsed
    
    if remain > 0:
        print(f"\nWaiting {remain:.1f} seconds before shutdown...")
        time.sleep(remain)
    else:
        print("\nTime is up, shutting down...")
    # =====================================================

    # خاموش کردن ویندوز
    os.system("shutdown /s /t 0")
