#!/usr/bin/env python3
"""
用法：python3 switch-event.py <分頁名稱>
範例：python3 switch-event.py 260607
"""

import json, subprocess, sys

import os
API_KEY  = os.environ.get("N8N_API_KEY") or open(".env").read().strip().split("N8N_API_KEY=")[-1].splitlines()[0]
BASE_URL = "https://hitorigs.zeabur.app"

# 三條需要更新的 workflow ID
WORKFLOW_IDS = {
    "報到-查詢票券": "YIJcZAAo6U95s54H",
    "報到-確認報到": "c6lb85w2uFtg9H8p",
    "報到-今日人數": "C7gnM6Nm92eJ3ZwF",
}

REMOVE_KEYS = {
    "active","createdAt","updatedAt","versionId","isArchived","triggerCount",
    "meta","parentFolderId","tags","shared","staticData","pinData",
    "activeVersionId","versionCounter","activeVersion","description","id"
}

def api(method, path, data=None):
    args = ["curl","-s","-X",method,f"{BASE_URL}{path}",
            "-H",f"X-N8N-API-KEY: {API_KEY}"]
    if data is not None:
        args += ["-H","Content-Type: application/json","-d",json.dumps(data)]
    r = subprocess.run(args, capture_output=True, text=True)
    return json.loads(r.stdout)

def update_sheet_name(wf_id, sheet_name):
    wf = api("GET", f"/api/v1/workflows/{wf_id}")
    for node in wf.get("nodes", []):
        if node["type"] == "n8n-nodes-base.googleSheets":
            node["parameters"]["sheetName"] = {
                "__rl": True, "mode": "name", "value": sheet_name
            }
    payload = {k: v for k, v in wf.items() if k not in REMOVE_KEYS}
    return api("PUT", f"/api/v1/workflows/{wf_id}", payload)

def reactivate(wf_id):
    api("POST", f"/api/v1/workflows/{wf_id}/deactivate")
    api("POST", f"/api/v1/workflows/{wf_id}/activate")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    sheet_name = sys.argv[1]
    print(f"切換至分頁：{sheet_name}\n")

    for name, wf_id in WORKFLOW_IDS.items():
        print(f"  更新 {name}...", end=" ")
        update_sheet_name(wf_id, sheet_name)
        reactivate(wf_id)
        print("✓")

    print(f"\n完成！三條 workflow 已切換至 {sheet_name}")
