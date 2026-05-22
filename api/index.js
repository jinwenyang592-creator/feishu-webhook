// api/index.js - 飞书Webhook代理
const COZE_API_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImE3N2U5MTA4LWJjYTktNGU1ZC04OGVkLTNlM2NiMWVkMzQzNiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIklwbnlhZ3kyOXhScE03RXVicWVnZXlodkt6N2RTUmlGIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc5NDYyMjc1LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjQxMjM0MjE2NjU4OTkzMTY3Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjQyNzMyMjc2OTQ5NzEyOTM0In0.eS6JN3I2iKezl1Mq-LorIYkytITVWQq1RAKJm4Yj6gc6jV3TS0oBl72BhZHCY_BqvNuSiiwPwzLiQNKiZU9Wo2EYENjBdOwGT5NsFlq7YrRRif31SbjRUXm9WINS51Aq37nDo1fsRavOp3LNqo-FGuBe-MD82Ssn4OXT-pyxOMxxlJ2RMBFLTL65MJJLA0njhrXMokdHIYoqR9eG_gYXwROkZDiyRmAOy9REXGbwrODcI6BgcyN2bNGsTLEMVKAs9DlZiOdQ2jiF1dS9iuDhfYBBp_eFV8ns6H0fD2URvZ1Z6PtNgoR9dXOylsovhQvFvif3jFGf-TVfb1kFT9EePA";
const COZE_API_URL = "https://zc7w5zpz2k.coze.site/run";
const FEISHU_APP_ID = "cli_aa8198f0d9399cbd";
const FEISHU_APP_SECRET = "TwvoUG8qejXISdKteVafYdD5aGOrUqcb";

export default async function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'GET') {
    return res.status(200).json({ status: 'ok' });
  }

  if (req.method === 'POST') {
    const body = req.body;
    
    // URL验证
    if (body.type === 'url_verification') {
      return res.status(200).json({ challenge: body.challenge });
    }
    
    return res.status(200).json({ msg: 'ok' });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
