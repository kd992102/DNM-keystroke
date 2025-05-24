const express = require('express');
const cors = require('cors');
const { google } = require('googleapis');
const fs = require('fs');
const { Readable } = require('stream');

const app = express();

// 啟用 CORS
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type']
}));

app.use(express.json());

// 從環境變數或檔案讀取憑證
let auth;
if (process.env.GOOGLE_CREDENTIALS) {
  auth = new google.auth.GoogleAuth({
    credentials: JSON.parse(process.env.GOOGLE_CREDENTIALS),
    scopes: ['https://www.googleapis.com/auth/drive.file']
  });
} else {
  auth = new google.auth.GoogleAuth({
    keyFile: './service-account.json',
    scopes: ['https://www.googleapis.com/auth/drive.file']
  });
}

// Google Drive 資料夾 ID
const folderId = process.env.FOLDER_ID || '1V0mHUym7i95R1Wzpcjm2hMn_8Nn2G-rl';

app.get('/', (req, res) => {
  res.json({ message: '伺服器運作中！' });
});

app.post('/upload', async (req, res) => {
  try {
    console.log('收到上傳請求：', req.body);

    const client = await auth.getClient();
    const drive = google.drive({ version: 'v3', auth: client });

    // 將 JSON 數據轉換為字串
    const jsonContent = JSON.stringify(req.body, null, 2);
    
    // 創建可讀流
    const stream = new Readable();
    stream.push(jsonContent);
    stream.push(null);

    const fileName = `typing_${Date.now()}.json`;

    const result = await drive.files.create({
      requestBody: {
        name: fileName,
        mimeType: 'application/json',
        parents: [folderId]
      },
      media: {
        mimeType: 'application/json',
        body: stream
      },
    });

    console.log('檔案上傳成功：', result.data.id);
    res.status(200).json({ success: true, fileId: result.data.id });
  } catch (err) {
    console.error('上傳錯誤：', err);
    res.status(500).json({ 
      success: false, 
      error: err.message,
      stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
    });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, '0.0.0.0', () => {
  console.log(`伺服器運行在 http://localhost:${port}`);
  if (process.env.NODE_ENV !== 'production') {
    console.log('支援的網路位址：');
    require('os').networkInterfaces()['Wi-Fi']?.forEach(interface => {
      if (interface.family === 'IPv4') {
        console.log(`http://${interface.address}:${port}`);
      }
    });
  }
});