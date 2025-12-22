"""
Test script to validate MLFlow endpoint authentication and payload format.
"""
import httpx
from databricks.sdk.core import Config

print("=" * 60)
print("Testing MLFlow Serving Endpoint Authentication")
print("=" * 60)

# Get auth headers using SDK Config
cfg = Config()
auth_headers = cfg.authenticate()

print(f"\n1. Auth headers type: {type(auth_headers)}")
print(f"   Auth headers keys: {list(auth_headers.keys()) if isinstance(auth_headers, dict) else 'Not a dict'}")
print(f"   Has Authorization: {'Authorization' in auth_headers if isinstance(auth_headers, dict) else 'N/A'}")

# Prepare request
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

print(f"\n2. Testing MLFlow endpoint...")
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
    print(f"   Headers: {dict(response.headers)}")
    print(f"   Body: {response.text[:500]}")

    if response.status_code == 200:
        data = response.json()
        print(f"\n[SUCCESS]")
        print(f"   Response data: {data}")
    else:
        print(f"\n[ERROR]: {response.status_code}")
        response.raise_for_status()

except httpx.HTTPStatusError as e:
    print(f"\n[HTTP Status Error]:")
    print(f"   Status: {e.response.status_code}")
    print(f"   Response body: {e.response.text}")
except Exception as e:
    print(f"\n[Error]: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
