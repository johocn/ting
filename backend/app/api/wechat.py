from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.wechat import WechatApp, WechatUser, WechatInviteCode
from app.schemas.wechat import WechatLoginRequest, WechatRegisterRequest

router = APIRouter(prefix="/wechat", tags=["wechat"])

@router.post("/login")
async def wechat_login(request: WechatLoginRequest, db: Session = Depends(get_db)):
    """微信登录"""
    # 获取微信应用配置
    wechat_app = db.query(WechatApp).filter(
        WechatApp.app_type == 'mini_program',  # 假设是小程序
        WechatApp.is_active == True
    ).first()
    
    if not wechat_app:
        raise HTTPException(status_code=400, detail="微信应用配置不存在")
    
    # 通过code获取session_key等信息
    import requests
    wx_response = requests.get(
        'https://api.weixin.qq.com/sns/jscode2session',
        params={
            'appid': wechat_app.app_id,
            'secret': wechat_app.app_secret,
            'js_code': request.code,
            'grant_type': 'authorization_code'
        }
    )
    
    wx_data = wx_response.json()
    
    if 'openid' not in wx_data:
        raise HTTPException(status_code=400, detail="微信登录失败")
    
    openid = wx_data['openid']
    session_key = wx_data.get('session_key')
    unionid = wx_data.get('unionid')
    
    # 验证用户信息（这里简化处理，实际需要验证签名和解密数据）
    # 验证签名
    import hashlib
    raw_data_md5 = hashlib.md5(request.raw_data.encode()).hexdigest()
    if raw_data_md5 != request.signature:
        raise HTTPException(status_code=400, detail="数据签名验证失败")
    
    # 检查是否已存在微信用户
    wechat_user = db.query(WechatUser).filter(
        WechatUser.open_id == openid,
        WechatUser.app_id == wechat_app.app_id
    ).first()
    
    if wechat_user:
        # 已存在的用户，直接登录
        from app.models.users import User
        user = db.query(User).filter(User.id == wechat_user.user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="用户数据异常")
        
        # 更新微信用户信息
        wechat_user.nickname = request.user_info.get('nickName')
        wechat_user.avatar_url = request.user_info.get('avatarUrl')
        wechat_user.gender = request.user_info.get('gender')
        wechat_user.city = request.user_info.get('city')
        wechat_user.province = request.user_info.get('province')
        wechat_user.country = request.user_info.get('country')
        wechat_user.language = request.user_info.get('language')
        db.commit()
        
        # 生成JWT token（这里简化处理）
        import jwt
        from datetime import datetime, timedelta
        from app.core.config import settings
        
        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }, settings.SECRET_KEY, algorithm="HS256")
        
        return {
            "user_info": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "integral": user.integral,
                "first_login": False
            },
            "token": token,
            "needs_phone_bind": not user.phone
        }
    else:
        # 新用户注册
        from app.models.users import User
        import hashlib
        
        # 创建系统用户
        user = User(
            username=request.user_info.get('nickName', f"微信用户_{openid[:8]}"),
            phone="",  # 初始为空，后续绑定
            integral=100  # 新用户奖励100积分
        )
        db.add(user)
        db.flush()  # 获取user.id
        
        # 创建微信用户记录
        wechat_user = WechatUser(
            union_id=unionid,
            open_id=openid,
            app_id=wechat_app.app_id,
            nickname=request.user_info.get('nickName'),
            avatar_url=request.user_info.get('avatarUrl'),
            gender=request.user_info.get('gender'),
            city=request.user_info.get('city'),
            province=request.user_info.get('province'),
            country=request.user_info.get('country'),
            language=request.user_info.get('language'),
            user_id=user.id
        )
        db.add(wechat_user)
        db.commit()
        
        # 生成JWT token
        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }, settings.SECRET_KEY, algorithm="HS256")
        
        return {
            "user_info": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "integral": user.integral,
                "first_login": True
            },
            "token": token,
            "needs_phone_bind": True  # 新用户需要绑定手机号
        }

@router.get("/my-invite")
async def get_my_wechat_invite(db: Session = Depends(get_db)):
    """获取我的微信邀请信息"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    from app.models.wechat import WechatUser
    wechat_user = db.query(WechatUser).filter(WechatUser.user_id == user_id).first()
    
    if not wechat_user:
        raise HTTPException(status_code=404, detail="微信用户信息不存在")
    
    # 如果没有邀请码，生成一个
    if not wechat_user.invite_code:
        import random
        import string
        invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        wechat_user.invite_code = invite_code
        db.commit()
    
    # 统计邀请数据
    from app.models.wechat import WechatInviteRecord
    invited_users = db.query(WechatInviteRecord).filter(
        WechatInviteRecord.inviter_open_id == wechat_user.open_id
    ).all()
    
    registered_count = len(invited_users)
    
    # 获取最新的邀请记录
    from app.models.users import User
    invite_records = []
    for record in invited_users[-10:]:  # 最近10个
        invitee_wechat_user = db.query(WechatUser).filter(
            WechatUser.open_id == record.invitee_open_id
        ).first()
        
        if invitee_wechat_user:
            invitee_user = db.query(User).filter(User.id == invitee_wechat_user.user_id).first()
            if invitee_user:
                invite_records.append({
                    "id": record.id,
                    "nickname": invitee_wechat_user.nickname,
                    "register_time": record.invite_time.isoformat() if record.invite_time else None,
                    "status": "activated" if invitee_user.phone else "registered"
                })
    
    return {
        "invite_code": wechat_user.invite_code,
        "share_url": f"https://yourapp.com/register?invite={wechat_user.invite_code}",
        "stats": {
            "total_invited": registered_count,
            "registered_count": registered_count,
            "active_count": sum(1 for r in invite_records if r['status'] == 'activated')
        },
        "records": invite_records
    }

@router.get("/apps", response_model=List[dict])
async def get_wechat_apps(db: Session = Depends(get_db)):
    """获取微信应用列表"""
    apps = db.query(WechatApp).filter(WechatApp.is_active == True).all()
    return apps

@router.post("/bind-phone")
async def bind_phone(
    phone: str,
    captcha: str,
    db: Session = Depends(get_db)
):
    """绑定手机号"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    from app.models.users import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 验证验证码（这里简化处理）
    # 实际应用中需要验证短信验证码
    if captcha != "123456":  # 仅为演示
        raise HTTPException(status_code=400, detail="验证码错误")
    
    user.phone = phone
    db.commit()
    
    # 同时更新微信用户表中的手机号
    from app.models.wechat import WechatUser
    wechat_user = db.query(WechatUser).filter(WechatUser.user_id == user_id).first()
    if wechat_user:
        wechat_user.phone_number = phone
        db.commit()
    
    return {"status": "success", "message": "绑定成功"}
