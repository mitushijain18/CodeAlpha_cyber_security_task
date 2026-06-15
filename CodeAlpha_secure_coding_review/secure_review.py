import hmac
import secrets
import hashlib
import json
from datetime import datetime, timezone
database = {
    "passes": [],
    "baseFareUSD": 15.00
}
SYSTEM_SECRET_KEY = b"C0d3A1ph4_Secur1ty_K3y_2026!"

def create_secure_bus_pass(passenger_id, pass_type):
    print(f"\n[SECURE RUN] Constructing verified pass metadata for: {passenger_id}")

    # Enforce server-side controlled pricing bounds
    final_price = database["baseFareUSD"]
    if pass_type.strip().lower() == 'monthly':
        final_price = database["baseFareUSD"] * 20 * 0.80
    pass_record = {
        "passId": "PASS-" + secrets.token_hex(4).upper(),
        "passengerId": passenger_id,
        "type": pass_type.capitalize(),
        "priceUSD": final_price,
        "issueDate": datetime.now(timezone.utc).isoformat(),
        "status": "ACTIVE"
    }

    token_payload = f"{pass_record['passId']}|{pass_record['passengerId']}|{pass_record['priceUSD']}"
    
    secure_hmac = hmac.new(SYSTEM_SECRET_KEY, token_payload.encode(), hashlib.sha256)
    pass_record["securitySignature"] = secure_hmac.hexdigest()

    database["passes"].append(pass_record)
    print("✔ Transaction signature locked with authentic HMAC key verification.")
    return pass_record

if __name__ == "__main__":
    print("=========================================")
    print("      SECURE AUDIT APP VERIFICATION      ")
    print("=========================================")
    user_id = input("Enter Passenger ID: ")
    ticket_type = input("Enter Pass Type (Single/Monthly): ")
    
    validated_pass = create_secure_bus_pass(user_id, ticket_type)
    print("\n--- Cryptographically Signed Output Payload ---")
    print(json.dumps(validated_pass, indent=4))