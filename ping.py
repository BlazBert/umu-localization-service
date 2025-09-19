"""
Quick-n-dirty client to “ping” the KNN Docker service.

• Adjust HOST and PORT if you mapped the container different.
• `sample` must hold every feature column the model expects, which are the columns listed below.
"""

import requests
import json
from pprint import pprint   # pretty print for the console

HOST = "localhost"   # or the container’s IP if you run on a swarm / k8s node
PORT = 8000          # host-side port is exposed: `docker run -p 8000:80 ... change accordingly`
URL  = f"http://{HOST}:{PORT}"

# 1) Optional health check – hit the OpenAPI spec
def health_check():
    try:
        r = requests.get(f"{URL}/openapi.json", timeout=3)
        r.raise_for_status()
        print("🟢 Service be alive ‘n kickin’!")
    except Exception as err:
        print("🔴 No answer from your FastAPI: ", err)
        raise

# 2) Craft one row of feature data (replace w/ your meassured data)
sample = {"nas_value_5g_signal_strength_rsrp":-77.0,
          "nas_value_5g_signal_strength_snr":285.0,
          "nas_value_nr5g_cell_information_global_cell_id":2373238784.0,
          "nas_value_nr5g_cell_information_physical_cell_id":51.0,
          "nas_value_nr5g_cell_information_rsrp":-760.0,
          "nas_value_nr5g_cell_information_rsrq":-110.0,
          "nas_value_nr5g_cell_information_snr":300.0,
          "nas_value_nr5g_cell_information_tracking_area_code":153.0,
          "throughput_upload_kb":21239.67,
          "throughput_download_kb":323.42}

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