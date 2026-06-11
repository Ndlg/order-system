# Collector Client

Minimal client scaffold for the future waybill collector.

The first version only defines the interface shape and can send heartbeat
payloads to the backend once collector endpoints become persistent.

```powershell
python client.py --base-url http://127.0.0.1:8000/api/v1 --collector-id local-dev
```
