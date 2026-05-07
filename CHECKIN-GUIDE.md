# Twitch Meetup 報到系統操作指南

## 活動前準備

1. 從報名系統匯出參加者名單 CSV
2. 將 CSV 匯入 Google Sheets，建立新分頁，以日期命名（如 `260607`）
3. 執行切換腳本：
   ```bash
   python3 switch-event.py 260607
   ```

## 活動當天

開啟 **https://hitorigs.github.io/meetup-checkin/**，按「開啟相機掃描」即可。

## 系統說明

| 元件 | 說明 |
|------|------|
| 前端 | https://hitorigs.github.io/meetup-checkin/ |
| Google Sheets | Sheet ID: `1K93cUNMpk4VuekLsBIPOIVqE01SZiqe2Ak9TdpB52_A` |
| n8n | https://hitorigs.zeabur.app |

### n8n Workflows

| 名稱 | ID | Webhook |
|------|----|---------|
| 報到-查詢票券 | `YIJcZAAo6U95s54H` | `POST /webhook/lookup` |
| 報到-確認報到 | `c6lb85w2uFtg9H8p` | `POST /webhook/confirm` |
| 報到-今日人數 | `C7gnM6Nm92eJ3ZwF` | `GET /webhook/count` |

## QR Code 格式

票券 QR code 掃出字串如 `590:52015`，系統取末五碼 `52015` 比對 Google Sheets 中 `TTA25052015` 的後五碼。

## 安全注意事項

- n8n API Key 存於本地 `.env`，不進 git
- 每次更換 API Key 後更新 `.env` 即可
