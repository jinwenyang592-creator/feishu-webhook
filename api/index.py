# -*- coding: utf-8 -*-
"""
Vercel Serverless Function - 飞书Webhook代理
"""

import json
import urllib.request
from http.server import BaseHTTPRequestHandler

# 配置信息
COZE_API_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImE3N2U5MTA4LWJjYTktNGU1ZC04OGVkLTNlM2NiMWVkMzQzNiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIklwbnlhZ3kyOXhScE03RXVicWVnZXlodkt6N2RTUmlGIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc5NDYyMjc1LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjQxMjM0MjE2NjU4OTkzMTY3Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjQyNzMyMjc2OTQ5NzEyOTM0In0.eS6JN3I2iKezl1Mq-LorIYkytITVWQq1RAKJm4Yj6gc6jV3TS0oBl72BhZHCY_BqvNuSiiwPwzLiQNKiZU9Wo2EYENjBdOwGT5NsFlq7YrRRif31SbjRUXm9WINS51Aq37nDo1fsRavOp3LNqo-FGuBe-MD82Ssn4OXT-pyxOMxxlJ2RMBFLTL65MJJLA0njhrXMokdHIYoqR9eG_gYXwROkZDiyRmAOy9REXGbwrODcI6BgcyN2bNGsTLEMVKAs9DlZiOdQ2jiF1dS9iuDhfYBBp_eFV8ns6H0fD2URvZ1Z6PtNgoR9dXOylsovhQvFvif3jFGf-TVfb1kFT9EePA"
COZE_API_URL = "https://zc7w5zpz2k.coze.site/run"
FEISHU_APP_ID = "cli_aa8198f0d9399cbd"
FEISHU_APP_SECRET = "TwvoUG8qejXISdKteVafYdD5aGOrUqcb"

class handler(BaseHTTPRequestHandler):
    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _read_body(self):
        length = self.headers.get('Content-Length')
        if length:
            return json.loads(self.rfile.read(int(length)).decode('utf-8'))
        return {}
    
    def do_GET(self):
        self._send_json(200, {'status': 'ok'})
    
    def do_POST(self):
        try:
            body = self._read_body()
            if body.get('type') == 'url_verification':
                self._send_json(200, {'challenge': body.get('challenge', '')})
                return
            self._send_json(200, {'msg': 'ok'})
        except Exception as e:
            self._send_json(500, {'error': str(e)})
