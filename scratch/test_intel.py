import sys, os
sys.path.insert(0, os.path.abspath("."))
from backend.pipeline import ingest_folder
from backend.report_intelligence import report_intelligence
import json

bundle = ingest_folder("data/final/uploads")
intel = report_intelligence(bundle)

print("Intel keys:", list(intel.keys()))
print("\n--- EXECUTIVE ---")
print(json.dumps(intel.get("executive"), indent=2))
print("\n--- NETWORK ---")
print(json.dumps(intel.get("network"), indent=2))
print("\n--- TEMPORAL ---")
print("coincidence_count:", intel.get("temporal", {}).get("coincidence_count"))
print("bursts:", intel.get("temporal", {}).get("bursts"))
print("rapid_in_out:", len(intel.get("temporal", {}).get("rapid_in_out", [])))
print("\n--- ML ---")
print("fitted:", intel.get("ml", {}).get("fitted"))
print("flagged:", intel.get("ml", {}).get("flagged"))
print("accounts count:", len(intel.get("ml", {}).get("accounts", [])))
print("\n--- STATISTICS ---")
print(json.dumps(intel.get("statistics"), indent=2))
print("\n--- RECOMMENDATIONS ---")
print(json.dumps(intel.get("recommendations"), indent=2))
