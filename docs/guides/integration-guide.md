# 集成指南

## 🔄 第三方集成

### 1. 微信集成

#### 1.1 微信登录集成

##### 1.1.1 前端集成

```javascript
// 微信登录函数
async function wechatLogin() {
  try {
    // 调用微信登录API
    const loginRes = await uni.login({
      provider: 'weixin',
      scopes: 'auth_user'
    });
    
    // 获取用户信息
    const userRes = await uni.getUserInfo({
      provider: 'weixin',
      scopes: 'auth_user'
    });
    
    // 发送登录请求
    const response = await this.$http.post('/api/auth/wechat/login', {
      code: loginRes.code,
      encrypted_data: userRes.encryptedData,
      iv: userRes.iv,
      raw_data: userRes.rawData,
      signature: userRes.signature
    });
    
    // 保存用户信息和token
    uni.setStorageSync('token', response.data.token);
    uni.setStorageSync('user_info', response.data.user_info);
    
    return response.data;
  } catch (error) {
    console.error('微信登录失败:', error);
    throw error;
  }
}
```

##### 1.1.2 后端集成

```python
from wechatpy import WeChatOAuth
import requests
from fastapi import APIRouter, HTTPException
from app.core.config import settings

@router.post("/wechat/login")
async def wechat_login(code: str, encrypted_data: str, iv: str):
    # 通过code获取access_token和openid
    token_url = f"https://api.weixin.qq.com/sns/jscode2session"
    params = {
        'appid': settings.WECHAT_APP_ID,
        'secret': settings.WECHAT_APP_SECRET,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    
    response = requests.get(token_url, params=params)
    wx_data = response.json()
    
    if 'openid' not in wx_data:
        raise HTTPException(status_code=400, detail="微信登录失败")
    
    # 验证并解密用户信息
    from wechatpy.crypto import WeChatCrypto
    crypto = WeChatCrypto(
        settings.WECHAT_APP_SECRET,
        settings.WECHAT_ENCODING_AES_KEY,
        settings.WECHAT_APP_ID
    )
    
    decrypted_data = crypto.decrypt_message(encrypted_data, iv, wx_data['session_key'])
    
    # 处理用户信息并登录/注册
    user = process_wechat_user(decrypted_data, wx_data['openid'])
    
    # 生成JWT token
    access_token = create_access_token(data={"user_id": user.id})
    
    return {
        "user_info": {
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "integral": user.integral
        },
        "token": access_token
    }
```

#### 1.2 微信分享集成

```javascript
// 微信分享配置
uni.onShareAppMessage(() => {
  return {
    title: '推荐一个学习赚钱的好平台',
    path: `/pages/index?invite_code=${this.inviteCode}`,
    imageUrl: '/static/share-image.jpg'
  }
});
```

### 2. 支付集成

#### 2.1 微信支付集成

```python
import wechatpy.pay
from wechatpy.pay import WeChatPay

def create_payment_order(product_id: int, user_id: int, amount: float):
    """创建微信支付订单"""
    wechat_pay = WeChatPay(
        appid=settings.WECHAT_PAY_APPID,
        api_key=settings.WECHAT_PAY_API_KEY,
        mch_id=settings.WECHAT_PAY_MCH_ID,
        mch_cert=settings.WECHAT_PAY_CERT_PATH,
        mch_key=settings.WECHAT_PAY_KEY_PATH
    )
    
    # 创建订单
    order = wechat_pay.order.create(
        body=f"商品支付 - {product_id}",
        out_trade_no=f"ORDER_{product_id}_{user_id}_{int(time.time())}",
        total_fee=int(amount * 100),  # 金额单位：分
        spbill_create_ip="127.0.0.1",
        notify_url=settings.WECHAT_PAY_NOTIFY_URL,
        trade_type="JSAPI",
        openid=get_user_openid(user_id)
    )
    
    # 生成支付参数
    pay_params = wechat_pay.jsapi.get_jsapi_params(
        prepay_id=order['prepay_id']
    )
    
    return {
        "order_id": order['out_trade_no'],
        "pay_params": pay_params
    }
```

#### 2.2 支付回调处理

```python
from fastapi import Request

@router.post("/payment/callback")
async def payment_callback(request: Request):
    """支付回调处理"""
    body = await request.body()
    
    # 验证签名
    if not verify_signature(body):
        return {"return_code": "FAIL", "return_msg": "签名验证失败"}
    
    # 解析支付结果
    xml_data = xmltodict.parse(body)
    result = xml_data['xml']
    
    if result['return_code'] == 'SUCCESS' and result['result_code'] == 'SUCCESS':
        # 处理支付成功逻辑
        order_id = result['out_trade_no']
        transaction_id = result['transaction_id']
        
        # 更新订单状态
        update_order_status(order_id, 'paid', transaction_id)
        
        # 发放商品
        process_product_delivery(order_id)
    
    return {"return_code": "SUCCESS", "return_msg": "OK"}
```

### 3. 短信服务集成

#### 3.1 阿里云短信集成

```python
import json
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models

def send_sms_verification_code(phone: str, code: str):
    """发送短信验证码"""
    config = open_api_models.Config(
        access_key_id=settings.ALIBABA_ACCESS_KEY_ID,
        access_key_secret=settings.ALIBABA_ACCESS_KEY_SECRET
    )
    config.endpoint = f"dysmsapi.aliyuncs.com"
    client = Dysmsapi20170525Client(config)
    
    send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
        phone_numbers=phone,
        sign_name=settings.SMS_SIGN_NAME,
        template_code=settings.SMS_TEMPLATE_CODE,
        template_param=json.dumps({"code": code})
    )
    
    try:
        response = client.send_sms(send_sms_request)
        return response.body
    except Exception as e:
        print(f"发送短信失败: {e}")
        return None
```

### 4. 邮件服务集成

#### 4.1 SMTP邮件发送

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_email(to_email: str, subject: str, content: str):
    """发送邮件"""
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"发送邮件失败: {e}")
        return False
```

### 5. 消息推送集成

#### 5.1 极光推送集成

```python
import jpush as jpush
from app.core.config import settings

def send_push_notification(registration_id: str, title: str, content: str):
    """发送推送通知"""
    _jpush = jpush.JPush(settings.JPUSH_APP_KEY, settings.JPUSH_MASTER_SECRET)
    push = _jpush.create_push()
    
    push.audience = jpush.registration_id(registration_id)
    push.notification = jpush.notification(alert=content)
    push.platform = jpush.all_
    
    try:
        response = push.send()
        return response
    except Exception as e:
        print(f"推送发送失败: {e}")
        return None
```

### 6. 文件存储集成

#### 6.1 阿里云OSS集成

```python
import oss2
from app.core.config import settings

def upload_file_to_oss(file_path: str, object_name: str):
    """上传文件到阿里云OSS"""
    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
    
    with open(file_path, 'rb') as file_obj:
        result = bucket.put_object(object_name, file_obj)
    
    if result.status == 200:
        return f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/{object_name}"
    else:
        return None

def generate_presigned_url(object_name: str, expiration: int = 3600):
    """生成预签名URL"""
    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
    
    return bucket.sign_url('GET', object_name, expiration)
```

### 7. 搜索服务集成

#### 7.1 Elasticsearch集成

```python
from elasticsearch import Elasticsearch
from app.core.config import settings

es_client = Elasticsearch([settings.ELASTICSEARCH_HOST])

def search_contents(query: str, category: str = None):
    """搜索内容"""
    search_body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"title": query}},
                    {"match": {"description": query}}
                ]
            }
        }
    }
    
    if category:
        search_body["query"]["bool"]["filter"] = [
            {"term": {"category": category}}
        ]
    
    result = es_client.search(index="contents", body=search_body)
    return result['hits']['hits']
```

### 8. 缓存集成

#### 8.1 Redis集成

```python
import redis
import json
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL)

def cache_get(key: str):
    """获取缓存"""
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def cache_set(key: str, value: any, expire: int = 3600):
    """设置缓存"""
    redis_client.setex(key, expire, json.dumps(value))

def cache_delete(key: str):
    """删除缓存"""
    redis_client.delete(key)

def cache_incr(key: str, amount: int = 1):
    """缓存计数器增加"""
    return redis_client.incr(key, amount)
```

### 9. 消息队列集成

#### 9.1 Celery任务队列

```python
from celery import Celery
from app.core.config import settings

celery_app = Celery('ting_tasks')
celery_app.conf.broker_url = settings.REDIS_URL
celery_app.conf.result_backend = settings.REDIS_URL

@celery_app.task
def process_video_upload(video_id: int):
    """处理视频上传任务"""
    # 1. 视频转码
    # 2. 生成缩略图
    # 3. 更新数据库
    # 4. 发送通知
    pass

@celery_app.task
def send_bulk_notifications(user_ids: list, message: str):
    """批量发送通知"""
    for user_id in user_ids:
        send_push_notification_to_user(user_id, message)
```

### 10. 监控集成

#### 10.1 Prometheus监控

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# 定义监控指标
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('api_request_duration_seconds', 'API request latency')
ACTIVE_USERS = Gauge('active_users', 'Number of active users')

def monitor_api_call(method: str, endpoint: str, duration: float):
    """监控API调用"""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    REQUEST_LATENCY.observe(duration)

# 在API中间件中使用
async def monitor_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    monitor_api_call(request.method, request.url.path, duration)
    
    return response
```

## 🛠️ 集成最佳实践

### 1. 错误处理

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_external_api(url: str, data: dict):
    """带重试机制的外部API调用"""
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"External API call failed: {e}")
        raise
```

### 2. 配置管理

```python
from pydantic_settings import BaseSettings

class IntegrationSettings(BaseSettings):
    # 微信配置
    WECHAT_APP_ID: str
    WECHAT_APP_SECRET: str
    WECHAT_PAY_APPID: str
    WECHAT_PAY_API_KEY: str
    WECHAT_PAY_MCH_ID: str
    
    # 短信配置
    ALIBABA_ACCESS_KEY_ID: str
    ALIBABA_ACCESS_KEY_SECRET: str
    SMS_SIGN_NAME: str
    SMS_TEMPLATE_CODE: str
    
    # OSS配置
    OSS_ACCESS_KEY_ID: str
    OSS_ACCESS_KEY_SECRET: str
    OSS_ENDPOINT: str
    OSS_BUCKET_NAME: str
    
    class Config:
        env_file = ".env"
```

### 3. 安全措施

```python
import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, secret: str):
    """验证Webhook签名"""
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, f"sha256={expected_signature}")
```

---

这些集成指南为第三方服务的接入提供了完整的参考，包括微信、支付、短信、邮件、推送、存储、搜索、缓存、消息队列和监控等各种服务的集成方式。
