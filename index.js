const express = require('express');
const fetch = require('node-fetch');
const app = express();

// ========== 配置区 ==========
const COZE_API_TOKEN = "sat_1SgflSM7tzKXzEL2IG3AEesujK8hl3Zb0gVYo366K9oKeUiYUAl9V7Wa7qrIaImK";
const COZE_API_URL = "https://zc7w5zpz2k.coze.site/run";
const FEISHU_APP_ID = "cli_aa8198f0d9399cbd";
const FEISHU_APP_SECRET = "TwvoUG8qejXISdKteVafYdD5aGOrUqcb";
const PORT = process.env.PORT || 3000;

// ========== 中间件 ==========
app.use(express.json());

// ========== 路由 ==========

// GET - 健康检查
app.get('/', (req, res) => {
  console.log('GET / - 健康检查');
  res.json({ status: 'ok', message: '飞书Webhook代理服务运行中', time: new Date().toISOString() });
});

// POST - 飞书事件
app.post('/', async (req, res) => {
  const body = req.body;
  console.log('POST / 收到请求:', JSON.stringify(body).substring(0, 200));
  
  try {
    // 1. URL验证 - 飞书配置时会发送
    if (body.type === 'url_verification') {
      const challenge = body.challenge || '';
      console.log('URL验证请求, challenge:', challenge);
      return res.status(200).json({ challenge: challenge });
    }
    
    // 2. 消息事件
    const header = body.header || {};
    if (header.event_type === 'im.message.receive_v1') {
      // 立即返回200，异步处理消息
      res.status(200).json({ msg: 'ok' });
      
      // 异步处理
      handleMessageEvent(body).catch(err => {
        console.error('处理消息异常:', err);
      });
      return;
    }
    
    // 3. 其他请求
    res.status(200).json({ msg: 'ok' });
    
  } catch (error) {
    console.error('处理请求异常:', error);
    res.status(500).json({ error: error.message });
  }
});

// ========== 业务函数 ==========

async function handleMessageEvent(eventData) {
  console.log('开始处理消息事件');
  
  const event = eventData.event || {};
  const sender = event.sender?.sender_id || {};
  const openId = sender.open_id || '';
  
  const message = event.message || {};
  const contentStr = message.content || '{}';
  
  let userInput = '';
  try {
    const content = typeof contentStr === 'string' ? JSON.parse(contentStr) : contentStr;
    userInput = content.text || '';
  } catch (e) {
    console.error('解析消息内容失败:', e);
    return;
  }
  
  console.log('用户消息:', userInput, 'openId:', openId);
  
  if (userInput) {
    try {
      const result = await callCozeAPI(userInput, openId);
      console.log('Coze返回:', JSON.stringify(result).substring(0, 200));
      
      if (result.response) {
        await sendFeishuMessage(openId, result.response);
      }
    } catch (error) {
      console.error('调用Coze API失败:', error);
      await sendFeishuMessage(openId, '系统繁忙，请稍后再试~');
    }
  }
}

async function callCozeAPI(userInput, userOpenid) {
  const response = await fetch(COZE_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${COZE_API_TOKEN}`
    },
    body: JSON.stringify({
      user_input: userInput,
      user_openid: userOpenid
    })
  });
  
  if (!response.ok) {
    throw new Error(`Coze API错误: ${response.status}`);
  }
  
  return response.json();
}

async function getFeishuToken() {
  const response = await fetch('https://open.larkoffice.com/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      app_id: FEISHU_APP_ID,
      app_secret: FEISHU_APP_SECRET
    })
  });
  
  const result = await response.json();
  if (result.code === 0) {
    return result.tenant_access_token;
  }
  throw new Error('获取飞书Token失败: ' + JSON.stringify(result));
}

async function sendFeishuMessage(openId, text) {
  try {
    const token = await getFeishuToken();
    console.log('获取飞书Token成功');
    
    const response = await fetch('https://open.larkoffice.com/open-apis/im/v1/messages?receive_id_type=open_id', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        receive_id: openId,
        msg_type: 'text',
        content: JSON.stringify({ text: text })
      })
    });
    
    const result = await response.json();
    console.log('发送飞书消息结果:', JSON.stringify(result));
  } catch (error) {
    console.error('发送飞书消息失败:', error);
  }
}

// ========== 启动服务 ==========
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 飞书Webhook代理服务启动成功!`);
  console.log(`📡 端口: ${PORT}`);
  console.log(`⏰ 时间: ${new Date().toISOString()}`);
});
