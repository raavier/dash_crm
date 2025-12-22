"""
Test script to validate Databricks connection with new SDK Config pattern.
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 60)
print("Testing Databricks Connection with SDK Config")
print("=" * 60)

# Load environment variables
from dotenv import load_dotenv
load_dotenv('backend/.env')

print("\n1. Environment Variables:")
print(f"   DATABRICKS_HOST: {os.getenv('DATABRICKS_HOST')}")
print(f"   DATABRICKS_WAREHOUSE_ID: {os.getenv('DATABRICKS_WAREHOUSE_ID')}")
print(f"   DATABRICKS_TOKEN: {'***' + os.getenv('DATABRICKS_TOKEN', '')[-4:] if os.getenv('DATABRICKS_TOKEN') else 'NOT SET'}")

try:
    print("\n2. Initializing Database Connection...")
    from backend.database import db
    print("   [OK] Database connection initialized")
    print(f"   Warehouse ID: {db.warehouse_id}")
    print(f"   Host: {db.cfg.host}")

    print("\n3. Testing Simple Query...")
    result = db.execute_query("SELECT 'Connection successful!' as message, current_timestamp() as timestamp")
    print(f"   [OK] Query executed successfully!")
    print(f"   Result: {result}")

    print("\n4. Testing Query with Parameters...")
    query = "SELECT :param1 as test_param, :param2 as test_value"
    params = {"param1": "test", "param2": 123}
    result = db.execute_query(query, params)
    print(f"   [OK] Parameterized query executed successfully!")
    print(f"   Result: {result}")

    print("\n" + "=" * 60)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("=" * 60)

except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 60)
    print("[FAILED] TESTS FAILED")
    print("=" * 60)
    sys.exit(1)
