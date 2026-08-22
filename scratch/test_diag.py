import sys, os
sys.path.insert(0, os.path.abspath("."))
import json

from backend.pipeline import ingest_folder
from backend.report_intelligence import report_intelligence
from backend import ml
from backend.fusion import rapid_payouts, correlate_phones, circular_flows, cached_fraud_heat

bundle = ingest_folder("data/final/uploads")
print(f"Loaded bundle: bank={len(bundle.get('bank', []))}, cdr={len(bundle.get('cdr', []))}, ipdr={len(bundle.get('ipdr', []))}")

# Test ML
ml_res = ml.ml_outliers(bundle)
print("ML outliers:", "fitted=", ml_res.get("fitted"), "count=", len(ml_res.get("accounts", [])))

# Test rapid payouts
rp = rapid_payouts(bundle)
print("Rapid payouts count:", len(rp))

# Test correlate phones
cp = correlate_phones(bundle)
print("Correlate phones hits:", len(cp.get("hits", [])))

# Test circular flows
cf = circular_flows(bundle)
print("Circular flows count:", len(cf))

# Test fraud heat round payouts
fh = cached_fraud_heat(bundle)
print("Fraud heat accounts:", len(fh.get("accounts", [])), "round payouts:", len(fh.get("round_payouts", [])))

# Test report intelligence
intel = report_intelligence(bundle)
print("\n--- Report Intelligence Results ---")
print("Executive Overall Risk:", intel["executive"]["overall_risk_score"], intel["executive"]["risk_band"])
print("Suspicious entities (Mule Nodes):", intel["executive"]["suspicious_entities"])
print("Network Hubs:", len(intel["network"]["hubs"]), "Bridges:", intel["network"]["bridges"], "Clusters:", intel["network"]["clusters"])
print("Temporal Coincidences:", intel["temporal"]["coincidence_count"])
print("Temporal Rapid In-Out:", intel["temporal"]["rapid_in_out_count"])
print("Circular Loops:", len(intel["circular"]["loops"]))
print("Circular Rapid Payouts:", len(intel["circular"]["rapid_payouts"]))
print("ML Fitted:", intel["ml"]["fitted"], "ML Flagged Accounts:", len(intel["ml"]["accounts"]))
print("Statistics Mean:", intel["statistics"]["mean"], "Max:", intel["statistics"]["max"], "Median:", intel["statistics"]["median"])
print("Statistics Top Senders:", len(intel["statistics"]["top_senders"]), "Top Receivers:", len(intel["statistics"]["top_receivers"]))
print("Recommendations Count:", len(intel["recommendations"]))
