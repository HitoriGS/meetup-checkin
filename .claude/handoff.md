# Handoff — 2026-05-07 23:59

## 現在在做什麼
Twitch Meetup QR code 報到系統已完整建立並上線。

## 馬上要做的事（優先順序）
1. 在 n8n 刪除舊的 API key（Settings → API → 刪除舊 key）
2. 下次活動前執行 `python3 switch-event.py <新分頁名稱>`

## 注意事項 / 踩坑紀錄
- 前端**不能**從 n8n webhook 托管：n8n 強制加 `Content-Security-Policy: sandbox`，會封鎖 `getUserMedia`
- iOS Safari 不支援 `BarcodeDetector`，掃描靠 `jsQR` + canvas fallback
- `style.display = ''` 無法覆蓋 CSS `display:none`，要用 `'block'`
- API key 不可寫在程式碼裡，讀 `.env`（已加入 `.gitignore`）

## 相關檔案
- `/Users/Asunplugged/coding/twitch-meetup-checkin/index.html` — 前端頁面（GitHub Pages）
- `/Users/Asunplugged/coding/twitch-meetup-checkin/switch-event.py` — 活動切換腳本
- `/Users/Asunplugged/coding/twitch-meetup-checkin/.env` — n8n API key（不進 git）
- `/Users/Asunplugged/coding/twitch-meetup-checkin/CHECKIN-GUIDE.md` — 操作說明

## 最後狀態
- branch: main，所有 commits 已 push
- 三條 n8n workflow 均 active
- Google Sheets 目前指向分頁 `260507`
- GitHub Pages：https://hitorigs.github.io/meetup-checkin/
