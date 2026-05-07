// ────────────────────────────────────────────────────────────
// n8n Workflow B — Lookup Ticket  (貼入 Code 節點)
//
// 節點順序：
//   [Webhook POST] → [Google Sheets: Get Many Rows] → [Code (此檔)] → [Respond to Webhook]
//
// Webhook 設定：
//   Method: POST  /  Path: lookup  /  Response Mode: Using 'Respond to Webhook' Node
//
// Google Sheets 節點設定：
//   Operation: Get Many Rows（讀取全部資料列）
//   Document ID: 你的 Google Sheet ID
//   Sheet Name: 存放名單的分頁名稱
//
// Respond to Webhook 節點設定：
//   Response Code: 200
//   Response Body: {{ JSON.stringify($json) }}
//   Add Header → Name: Content-Type / Value: application/json
//   Add Header → Name: Access-Control-Allow-Origin / Value: *
// ────────────────────────────────────────────────────────────

// 從 Webhook body 取得末五碼
const suffix = ($('Webhook').first().json.body?.suffix || '').trim();

// 驗證：必須是 5 位數字
if (!/^\d{5}$/.test(suffix)) {
  return [{ json: { found: false, error: 'invalid_suffix' } }];
}

// 取得 Google Sheets 讀出的所有資料列
const rows = $input.all();

// 找出票券編號末五碼相符的那一列
const match = rows.find(row => {
  const ticketNum = (row.json['Ticket number'] || '').trim();
  return ticketNum.length >= 5 && ticketNum.slice(-5) === suffix;
});

if (!match) {
  return [{ json: { found: false } }];
}

// 判斷是否已報到：Checkin Date (UTC) 欄位有值即代表已報到
const rawDate = (match.json['Checkin Date (UTC)'] || '').trim();
const isCheckedIn = rawDate !== '';

// 姓名優先用 First Name，備用 Paid by (name)
const name = (match.json['First Name'] || match.json['Paid by (name)'] || '未知').trim();

return [{
  json: {
    found: true,
    checkedIn: isCheckedIn,
    name: name,
    ticketNumber: match.json['Ticket number'].trim(),
    checkinTime: isCheckedIn ? rawDate : null
  }
}];
