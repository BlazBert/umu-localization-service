"""
Quick-n-dirty client to “ping” the localization Docker service.

• Adjust HOST and PORT if you mapped the container different.
• `sample` must hold every feature column the model expects.
"""

import requests
import json
from pprint import pprint   # pretty print for the console

HOST = "localhost"   # or the container’s IP if you run on a swarm / k8s node
PORT = 8000          # host-side port is exposed: `docker run -p 8000:80 ...`
URL  = f"http://{HOST}:{PORT}"

# 1) Optional health check – hit the OpenAPI spec
def health_check():
    try:
        r = requests.get(f"{URL}/openapi.json", timeout=3)
        r.raise_for_status()
        print("🟢 Service be alive ‘n kickin’!")
    except Exception as err:
        print("🔴 No answer from yer FastAPI ship:", err)
        raise

# 2) Craft one row of feature data (replace w/ your real column names)

sample = {"CL":-77.0,
          "mcs_ul":15.0,
          "phr":153.0,
          "pl":21239.67,
          "mcs_dl":20.0,
          "txok":1.0,
          "retx_dl":0.0,
          "brate_ul":2373238784.0,
          "rxok":1.0,
          "cqi":51.0,
          "snr":-95.0,
          "ri":1.0,
          "retx_ul":0.0,
          "ta":0.0,
          }

def predict(features: dict):
    r = requests.post(f"{URL}/predict", json=features, timeout=5)
    r.raise_for_status()           # blow up if code ≥400
    return r.json()

if __name__ == "__main__":
    
    health_check()

    print("📡  Firing /predict …")
    result = predict(sample)
    print("🎯  Model’s reply:")
    pprint(result)  