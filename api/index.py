# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import json
import urllib.request

COZE_API_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImE3N2U5MTA4LWJjYTktNGU1ZC04OGVkLTNlM2NiMWVkMzQzNiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIkhwbnlhZ3kyOXhScE03RXVicWVnZXlodkt6N2RTUmlGIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc5NDYyMjc1LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjQxMjM0MjE2NjU4OTkzMTY3Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjQyNzMyMjc2OTQ5NzEyOTM0In0.eS6JN3I2iKezl1Mq-LorIYkytITVWQq1RAKJm4Yj6gc6jV3TS0oBl72BhZHCY_BqvNuSiiwPwzLiQNKiZU9Wo2EYENjBdOwGT5NsFlq7YrRRif31SbjRUXm9WINS51Aq37nDo1fsRavOp3LNqo-FGuBe-MD82Ssn4OXT-pyxOMxxlJ2RMBFLTL65MJJLA0njhrXMokdHIYoqR9eG_gYXwROkZDiyRmAOy9REXGbwrODcI6BgcyN2bNGsTLEMVKAs9DlZiOdQ2jiF1dS9iuDhfYBBp_eFV8ns6H0fD2URvZ1Z6PtNgoR9dXOylsovhQvFvif3jFGf-TVfb1kFT9EePA"
COZE_API_URL = "https://zc7w5zpz2k.coze.site/run"
FEISHU_APP_ID = "cli_aa8198f0d9399cbd"
FEISHU_APP_SECRET = "TwvoUG8qejXISdKteVafYdD5aGOrUqcb"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        # URL验证
        if data.get('type') == 'url_verification':
            self._send_json({'challenge': data.get('challenge', '')})
            return
        
        # 处理消息
        if data.get('header', {}).get('event_type') == 'im.message.receive_v1':
            self._handle_message(data)
        
        self._send_json({'msg': 'ok'})
    
    def do_GET(self):
        self._send_json({'status': 'ok'})
    
    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _handle_message(self, data):
        event = data.get('event', {})
        sender = event.get('sender', {}).get('sender_id', {})
        open_id = sender.get('open_id', '')
        
        message = event.get('message', {})
        content_str = message.get('content', '{}')
        
        try:
            content = json.loads(content_str) if isinstance(content_str, str) else content_str
            user_input = content.get('text', '')
        except:
            user_input = ''
        
        if user_input:
            try:
                result = self._call_coze(user_input, open_id)
                if result.get('response'):
                    self._send_feishu(open_id, result['response'])
            except Exception as e:
                self._send_feishu(open_id, "系统繁忙~")
    
    def _call_coze(self, user_input, user_openid):
        req = urllib.request.Request(
            COZE_API_URL,
            data=json.dumps({"user_input": user_input, "user_openid": user_openid}).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {COZE_API_TOKEN}'
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    
    def _send_feishu(self, open_id, text):
        req = urllib.request.Request(
            "https://open.larkoffice.com/open-apis/auth/v3/tenant_access_token/internal",
            data=json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            token = result.get('tenant_access_token', '') if result.get('code') == 0 else ''
        
        if not token:
            return
        
        req = urllib.request.Request(
            "https://open.larkoffice.com/open-apis/im/v1/messages?receive_id_type=open_id",
            data=json.dumps({
                "receive_id": open_id,
                "msg_type": "text",
                "content": json.dumps({"text": text}, ensure_ascii=False)
            }).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            method='POST'
        )
        urllib.request.urlopen(req, timeout=30)
