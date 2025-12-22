"""
Test MLFlow endpoint with service principal authentication (simulating production).
This tests if the service principal token works differently than personal token.
"""
import httpx
import os

print("=" * 60)
print("Testing Service Principal Authentication")
print("=" * 60)

# Simulate production environment
os.environ['DATABRICKS_HOST'] = 'adb-116288240407984.4.azuredatabricks.net'

# Import AFTER setting env vars to ensure Config picks them up
from databricks.sdk.core import Config

print("\n1. Testing with current credentials...")
cfg = Config()
print(f"   Host: {cfg.host}")
print(f"   Auth type: {type(cfg.authenticate())}")

auth_headers = cfg.authenticate()
print(f"   Auth headers: {list(auth_headers.keys())}")

# Test endpoint
endpoint_url = "https://adb-116288240407984.4.azuredatabricks.net/serving-endpoints/connect_bot_prd/invocations"
headers = {
    **auth_headers,
    "Content-Type": "application/json"
}

payload = {
    "inputs": {
        "user_id": "flavio.assis@vale.com",
        "query": "oi"
    }
}

print(f"\n2. Calling MLFlow endpoint...")
print(f"   URL: {endpoint_url}")
print(f"   Payload: {payload}")

try:
    response = httpx.post(
        endpoint_url,
        headers=headers,
        json=payload,
        timeout=30.0
    )

    print(f"\n3. Response:")
    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"   [SUCCESS] Response: {data}")
    else:
        print(f"   [ERROR] Status: {response.status_code}")
        print(f"   Response body: {response.text}")
        print(f"   Response headers: {dict(response.headers)}")

except Exception as e:
    print(f"\n[Error]: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
