import sys, os
sys.path.insert(0, os.path.abspath("."))
from backend.pipeline import ingest_folder
import time

bundle = ingest_folder("data/final/uploads")
bank = bundle.get("bank", [])
cdr = bundle.get("cdr", [])
ipdr = bundle.get("ipdr", [])

print(f"Dataset stats: {len(bank)} bank, {len(cdr)} cdr, {len(ipdr)} ipdr")

# 1. Round transactions check
round_1000 = [r for r in bank if float(r.get("debit") or r.get("credit") or 0) >= 500 and float(r.get("debit") or r.get("credit") or 0) % 1000 == 0]
round_500 = [r for r in bank if float(r.get("debit") or r.get("credit") or 0) >= 500 and float(r.get("debit") or r.get("credit") or 0) % 500 == 0]
round_100 = [r for r in bank if float(r.get("debit") or r.get("credit") or 0) >= 100 and float(r.get("debit") or r.get("credit") or 0) % 100 == 0]
round_int = [r for r in bank if float(r.get("debit") or r.get("credit") or 0) >= 100 and float(r.get("debit") or r.get("credit") or 0).is_integer()]
print(f"Round txns: % 1000 = {len(round_1000)}, % 500 = {len(round_500)}, % 100 = {len(round_100)}, integer = {len(round_int)}")
print("Sample amounts in bank:", [r.get("debit") or r.get("credit") for r in bank[:15]])

# 2. Rapid payouts check: check accounts with debits in windows
by_acc = {}
for r in bank:
    acc = r.get("account_no")
    if not acc: continue
    d = float(r.get("debit") or 0)
    ts = float(r.get("ts") or 0)
    if d > 0 and ts > 0:
        by_acc.setdefault(acc, []).append((ts, d, r))

print(f"Unique debit accounts: {len(by_acc)}")
for w_min, thresh in [(15, 2), (30, 3), (60, 3), (60, 4), (60, 5), (1440, 5)]:
    rapid_matches = []
    for acc, txns in by_acc.items():
        if len(txns) < thresh: continue
        txns.sort(key=lambda x: x[0])
        n = len(txns)
        for i in range(n):
            j = i
            while j < n and txns[j][0] - txns[i][0] <= w_min * 60:
                j += 1
            if j - i >= thresh:
                rapid_matches.append((acc, j - i, sum(t[1] for t in txns[i:j])))
                break
    print(f"Rapid debits (window={w_min}m, thresh={thresh}): {len(rapid_matches)} accounts")

# 3. Timing report_intelligence
from backend.report_intelligence import report_intelligence
t0 = time.time()
intel = report_intelligence(bundle)
t1 = time.time()
print(f"\nreport_intelligence execution time: {t1 - t0:.2f}s")
