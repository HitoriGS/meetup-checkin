## 2026-05-07 Twitch Meetup QR code 報到系統

### 學到的事
- n8n webhook 回傳的 HTML 有強制 CSP sandbox（無 allow-same-origin），`getUserMedia` 會拋 TypeError，前端必須另外托管
- iOS Safari 不支援 `BarcodeDetector`，需搭配 `jsQR` + canvas 逐幀解析作 fallback
- `style.display = ""` 會讓 CSS `display:none` 重新生效，要明確設 `"block"`
- n8n API v1 無法列出 credentials，建立 workflow 時 Google Sheets 節點要讓使用者手動選一次
- n8n Variables 需付費授權，免費替代方案：本地 Python 腳本透過 REST API 批次更新 workflow

### 重要決策
- 前端用 GitHub Pages（無 CSP 限制），後端留在 n8n（三條 webhook）
- 換活動只需執行 `switch-event.py <分頁名稱>`，一次更新三條 workflow
- 今日人數從 Google Sheets Checkin Date 欄位即時計算，跨設備同步

### 已知問題 / 技術債
- git history 中殘留一把舊 n8n API key（已失效，但記得定期 rotate）
- `switch-event.py` 內有 Workflow ID 硬編碼，改 workflow 名稱需同步更新腳本

---

