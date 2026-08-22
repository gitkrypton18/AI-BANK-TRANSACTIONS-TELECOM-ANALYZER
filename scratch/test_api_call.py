import urllib.request
import json

def fetch():
    # Try logging in
    login_req = urllib.request.Request(
        "http://127.0.0.1:8000/auth/login",
        data=json.dumps({"username": "officer", "password": "password"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    token = None
    try:
        with urllib.request.urlopen(login_req) as resp:
            data = json.loads(resp.read().decode())
            token = data.get("access_token") or data.get("token")
            print("Logged in successfully, token:", token[:15] if token else "none")
    except Exception as e:
        print("Login failed:", e)

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    endpoints = [
        "/summary",
        "/payouts",
        "/flows/patterns?min_amount=10000",
        "/ml/outliers?contamination=0.05",
        "/reports/intelligence"
    ]

    for ep in endpoints:
        req = urllib.request.Request(f"http://127.0.0.1:8000{ep}", headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                print(f"\n=== {ep} === (Status 200)")
                if ep == "/summary":
                    print("  bank_records:", data.get("bank_records"), "entities:", data.get("entities"))
                elif ep == "/payouts":
                    print("  rapid count:", len(data.get("rapid", [])), "round count:", len(data.get("round", [])))
                    if data.get("rapid"): print("  sample rapid:", data["rapid"][0])
                    if data.get("round"): print("  sample round:", data["round"][0])
                elif ep.startswith("/flows/patterns"):
                    print("  circular:", len(data.get("circular", [])), "rapid_in_out:", len(data.get("rapid_in_out", [])))
                elif ep.startswith("/ml/outliers"):
                    print("  fitted:", data.get("fitted"), "count:", len(data.get("accounts", [])))
                elif ep == "/reports/intelligence":
                    print("  executive risk:", data.get("executive", {}).get("overall_risk_score"), data.get("executive", {}).get("risk_band"))
                    print("  suspicious entities:", data.get("executive", {}).get("suspicious_entities"))
                    print("  network hubs:", len(data.get("network", {}).get("hubs", [])))
                    print("  temporal coincidence count:", data.get("temporal", {}).get("coincidence_count"))
                    print("  circular loops:", len(data.get("circular", {}).get("loops", [])))
                    print("  circular rapid payouts:", len(data.get("circular", {}).get("rapid_payouts", [])))
                    print("  ml fitted:", data.get("ml", {}).get("fitted"), "ml accounts:", len(data.get("ml", {}).get("accounts", [])))
                    print("  stats mean:", data.get("statistics", {}).get("mean"), "median:", data.get("statistics", {}).get("median"), "max:", data.get("statistics", {}).get("max"))
                    print("  recs:", len(data.get("recommendations", [])))
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            print(f"\n=== {ep} === (FAILED {e.code}): {body}")
        except Exception as e:
            print(f"\n=== {ep} === (ERROR): {e}")

if __name__ == "__main__":
    fetch()
