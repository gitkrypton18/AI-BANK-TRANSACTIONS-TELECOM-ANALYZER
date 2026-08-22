import sys, os
sys.path.insert(0, os.path.abspath("."))
from starlette.testclient import TestClient
from backend.main import app
from backend.auth import create_access_token
from backend.pipeline import ingest_folder
import backend.api as api_mod

# Ingest data into state if not already present
if "bundle" not in api_mod._state or not api_mod._state["bundle"].get("bank"):
    api_mod._state["bundle"] = ingest_folder("data/final/uploads")

client = TestClient(app)
token = create_access_token({"sub": "officer", "role": "officer"})
headers = {"Authorization": f"Bearer {token}"}

print("=== TESTING ENDPOINTS ===")

# 1. /summary
r = client.get("/summary", headers=headers)
print("GET /summary:", r.status_code)
if r.status_code == 200:
    s = r.json()
    print("  bank_records:", s.get("bank_records"), "accounts:", s.get("entities", {}).get("accounts"))

# 2. /payouts
r = client.get("/payouts", headers=headers)
print("GET /payouts:", r.status_code)
if r.status_code == 200:
    p = r.json()
    print("  rapid count:", len(p.get("rapid", [])), "round count:", len(p.get("round", [])))
    if p.get("rapid"):
        print("  sample rapid payout:", p["rapid"][0])
    if p.get("round"):
        print("  sample round payout:", p["round"][0])

# 3. /ml/outliers
r = client.get("/ml/outliers?contamination=0.05", headers=headers)
print("GET /ml/outliers:", r.status_code)
if r.status_code == 200:
    m = r.json()
    print("  fitted:", m.get("fitted"), "count:", len(m.get("accounts", [])))
    if m.get("accounts"):
        print("  top outlier account:", m["accounts"][0])

# 4. /flows/patterns
r = client.get("/flows/patterns?min_amount=10000", headers=headers)
print("GET /flows/patterns:", r.status_code)
if r.status_code == 200:
    f = r.json()
    print("  circular loops:", len(f.get("circular", [])), "rapid in-out:", len(f.get("rapid_in_out", [])))

# 5. /reports/intelligence
r = client.get("/reports/intelligence", headers=headers)
print("GET /reports/intelligence:", r.status_code)
if r.status_code == 200:
    intel = r.json()
    print("  Risk Score:", intel.get("executive", {}).get("overall_risk_score"), intel.get("executive", {}).get("risk_band"))
    print("  Suspicious entities (Mule Nodes):", intel.get("executive", {}).get("suspicious_entities"))
    print("  Network Hubs:", len(intel.get("network", {}).get("hubs", [])), "Bridges:", intel.get("network", {}).get("bridges"), "Clusters:", intel.get("network", {}).get("clusters"))
    print("  Temporal Coincidences:", intel.get("temporal", {}).get("coincidence_count"))
    print("  Temporal Rapid in-out:", intel.get("temporal", {}).get("rapid_in_out_count"))
    print("  Circular Loops:", len(intel.get("circular", {}).get("loops", [])))
    print("  Circular Rapid Payouts:", len(intel.get("circular", {}).get("rapid_payouts", [])))
    print("  ML Fitted:", intel.get("ml", {}).get("fitted"), "ML Accounts:", len(intel.get("ml", {}).get("accounts", [])))
    print("  Statistics Mean:", intel.get("statistics", {}).get("mean"), "Median:", intel.get("statistics", {}).get("median"), "Max:", intel.get("statistics", {}).get("max"))
    print("  Recommendations:", len(intel.get("recommendations", [])))
else:
    print("  Error:", r.text)
