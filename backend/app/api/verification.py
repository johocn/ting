from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.mall import ExchangeRecord, Store, VerificationRecord, StoreEmployee
from app.schemas.verification import VerificationRequest

router = APIRouter(prefix="/verification", tags=["verification"])

@router.get("/store-info", response_model=dict)
async def get_store_info(db: Session = Depends(get_db)):
    """获取门店信息"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取员工信息
    employee = db.query(StoreEmployee).filter(
        StoreEmployee.user_id == user_id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="未找到门店信息")
    
    store = db.query(Store).filter(Store.id == employee.store_id).first()
    
    return {
        "store": {
            "id": store.id,
            "name": store.name,
            "address": store.address,
            "phone": store.phone
        }
    }

@router.get("/dashboard-stats", response_model=dict)
async def get_verification_stats(db: Session = Depends(get_db)):
    """获取核销统计信息"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取员工信息
    employee = db.query(StoreEmployee).filter(
        StoreEmployee.user_id == user_id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="未找到门店信息")
    
    store_id = employee.store_id
    
    from datetime import datetime
    # 今日核销数量
    from sqlalchemy import and_, func
    today_start = datetime.combine(datetime.today().date(), datetime.min.time())
    
    today_verifications = db.query(VerificationRecord).filter(
        VerificationRecord.store_id == store_id,
        VerificationRecord.verification_time >= today_start
    ).count()
    
    # 本月核销数量
    from datetime import datetime
    month_start = datetime.combine(datetime.today().replace(day=1), datetime.min.time())
    
    month_verifications = db.query(VerificationRecord).filter(
        VerificationRecord.store_id == store_id,
        VerificationRecord.verification_time >= month_start
    ).count()
    
    return {
        "today_count": today_verifications,
        "month_count": month_verifications
    }

@router.get("/recent", response_model=List[dict])
async def get_recent_verifications(
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """获取近期核销记录"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    employee = db.query(StoreEmployee).filter(
        StoreEmployee.user_id == user_id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="未找到门店信息")
    
    store_id = employee.store_id
    
    verifications = db.query(VerificationRecord).filter(
        VerificationRecord.store_id == store_id
    ).order_by(VerificationRecord.verification_time.desc()).limit(limit).all()
    
    result = []
    for verification in verifications:
        exchange_record = db.query(ExchangeRecord).filter(
            ExchangeRecord.id == verification.exchange_record_id
        ).first()
        
        result.append({
            "id": verification.id,
            "exchange_record": {
                "product_name": exchange_record.product.name if exchange_record else "未知商品"
            },
            "customer_name": "客户信息",  # 实际应从用户信息获取
            "verification_time": verification.verification_time.isoformat()
        })
    
    return result

@router.get("/detail", response_model=dict)
async def get_verification_detail(
    code: str, 
    db: Session = Depends(get_db)
):
    """获取核销详情"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    employee = db.query(StoreEmployee).filter(
        StoreEmployee.user_id == user_id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="未找到门店信息")
    
    store_id = employee.store_id
    
    # 查找兑换记录
    exchange_record = db.query(ExchangeRecord).filter(
        ExchangeRecord.exchange_code == code
    ).first()
    
    if not exchange_record:
        raise HTTPException(status_code=404, detail="兑换码不存在")
    
    # 检查权限：只能核销本店的商品
    # 实际应用中需要关联产品和门店的关系
    # 这里简化处理
    
    from app.models.mall import Product
    product = db.query(Product).filter(Product.id == exchange_record.product_id).first()
    
    return {
        "detail": {
            "id": exchange_record.id,
            "product": {
                "name": product.name if product else "未知商品",
                "description": product.description if product else ""
            },
            "exchange_code": exchange_record.exchange_code,
            "exchange_time": exchange_record.exchange_time.isoformat(),
            "validity_start_date": exchange_record.validity_start_date.isoformat() if exchange_record.validity_start_date else "",
            "validity_end_date": exchange_record.validity_end_date.isoformat() if exchange_record.validity_end_date else "",
            "status": exchange_record.status,
            "customer_info": "客户信息"  # 实际应从用户信息获取
        }
    }

@router.post("/confirm", response_model=dict)
async def confirm_verification(
    request: VerificationRequest, 
    db: Session = Depends(get_db)
):
    """确认核销"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取兑换记录
    exchange_record = db.query(ExchangeRecord).filter(
        ExchangeRecord.id == request.exchange_record_id
    ).first()
    
    if not exchange_record:
        raise HTTPException(status_code=404, detail="兑换记录不存在")
    
    if exchange_record.status != 'confirmed':
        raise HTTPException(status_code=400, detail="兑换记录状态异常")
    
    # 检查权限
    employee = db.query(StoreEmployee).filter(
        StoreEmployee.user_id == user_id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="未找到门店信息")
    
    # 创建核销记录
    from datetime import datetime
    verification_record = VerificationRecord(
        exchange_record_id=request.exchange_record_id,
        store_id=employee.store_id,
        verifier_user_id=user_id,
        verification_code=request.verification_code or f"VER_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    db.add(verification_record)
    
    # 更新兑换记录状态
    exchange_record.status = 'used'
    
    db.commit()
    
    return {"status": "success", "message": "核销成功"}

@router.get("/generate-qrcode", response_model=dict)
async def generate_qr_code(data: str):
    """生成二维码"""
    import qrcode
    import io
    import base64
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    return {"qr_code": f"data:image/png;base64,{img_base64}"}
