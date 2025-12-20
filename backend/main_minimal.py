"""
Minimal FastAPI app for testing Databricks Apps deployment
"""
print("=" * 60)
print("MINIMAL APP: Starting...")
print("=" * 60)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Minimal app is running!"}

@app.get("/health")
def health():
    return {"healthy": True}

print("MINIMAL APP: FastAPI app created successfully!")
print("=" * 60)
