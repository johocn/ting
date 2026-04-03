from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.mall import ProductCategory, Product, ExchangeRecord, Store
from app.schemas.mall import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/categories", response_model=List[dict])
async def get_product_categories(db: Session = Depends(get_db)):
    """获取商品分类列表"""
    categories = db.query(ProductCategory).filter(
        ProductCategory.is_active == True
    ).all()
    return categories

@router.get("/", response_model=List[dict])
async def get_products(
    category_id: int = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """获取商品列表"""
    query = db.query(Product).filter(Product.is_active == True)
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    products = query.offset(skip).limit(limit).all()
    result = []
    for product in products:
        product_dict = {}
        for column in product.__table__.columns:
            value = getattr(product, column.name)
            if hasattr(value, 'isoformat'):
                product_dict[column.name] = value.isoformat()
            else:
                product_dict[column.name] = value
        result.append(product_dict)
    return result

@router.get("/{product_id}", response_model=dict)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取单个商品详情"""
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    return product

@router.post("/", response_model=dict)
async def create_product(
    product_data: ProductCreate, 
    db: Session = Depends(get_db)
):
    """创建商品"""
    # 检查分类是否存在
    if product_data.category_id:
        category = db.query(ProductCategory).filter(
            ProductCategory.id == product_data.category_id,
            ProductCategory.is_active == True
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="商品分类不存在")
    
    db_product = Product(**product_data.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.put("/{product_id}", response_model=dict)
async def update_product(
    product_id: int, 
    product_update: ProductUpdate, 
    db: Session = Depends(get_db)
):
    """更新商品信息"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    return product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """删除商品（软删除）"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    product.is_active = False
    db.commit()
    return {"message": "商品删除成功"}

@router.post("/{product_id}/exchange", response_model=dict)
async def exchange_product(
    product_id: int, 
    quantity: int = 1, 
    db: Session = Depends(get_db)
):
    """兑换商品"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取商品信息
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    if product.stock_quantity < quantity:
        raise HTTPException(status_code=400, detail="库存不足")
    
    # 检查用户积分是否足够
    from app.models.points import UserPointAccount
    user_account = db.query(UserPointAccount).filter(
        UserPointAccount.user_id == user_id
    ).first()
    
    if not user_account:
        raise HTTPException(status_code=404, detail="用户积分账户不存在")
    
    total_cost = product.points_required * quantity
    if user_account.available_points < total_cost:
        raise HTTPException(status_code=400, detail="积分不足")
    
    # 扣减用户积分
    user_account.available_points -= total_cost
    user_account.frozen_points += total_cost  # 先冻结积分
    
    # 生成兑换码
    import random
    import string
    exchange_code = 'EX' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # 创建兑换记录
    from datetime import datetime, timedelta
    exchange_record = ExchangeRecord(
        user_id=user_id,
        product_id=product.id,
        points_deducted=total_cost,
        quantity=quantity,
        exchange_code=exchange_code,
        validity_start_date=datetime.utcnow(),
        validity_end_date=datetime.utcnow() + timedelta(days=product.validity_period_days or 30)
    )
    
    db.add(exchange_record)
    db.commit()
    
    # 实际扣减积分并更新状态
    user_account.frozen_points -= total_cost
    db.commit()
    
    return {
        "exchange_record_id": exchange_record.id,
        "exchange_code": exchange_code,
        "product_name": product.name,
        "points_deducted": total_cost,
        "validity_period": f"{product.validity_period_days or 30}天",
        "status": "confirmed"
    }

@router.get("/exchange/records", response_model=List[dict])
async def get_exchange_records(
    status: str = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """获取兑换记录"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    query = db.query(ExchangeRecord).filter(ExchangeRecord.user_id == user_id)
    
    if status:
        query = query.filter(ExchangeRecord.status == status)
    
    records = query.offset(skip).limit(limit).all()
    
    result = []
    for record in records:
        product = db.query(Product).filter(Product.id == record.product_id).first()
        result.append({
            "id": record.id,
            "product_name": product.name if product else "未知商品",
            "points_deducted": record.points_deducted,
            "quantity": record.quantity,
            "exchange_code": record.exchange_code,
            "exchange_time": record.exchange_time,
            "status": record.status,
            "validity_start_date": record.validity_start_date,
            "validity_end_date": record.validity_end_date
        })
    
    return result

@router.get("/exchange/record/{record_id}", response_model=dict)
async def get_exchange_record(record_id: int, db: Session = Depends(get_db)):
    """获取单个兑换记录详情"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    record = db.query(ExchangeRecord).filter(
        ExchangeRecord.id == record_id,
        ExchangeRecord.user_id == user_id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="兑换记录不存在")
    
    product = db.query(Product).filter(Product.id == record.product_id).first()
    
    return {
        "id": record.id,
        "product_name": product.name if product else "未知商品",
        "product_description": product.description if product else "",
        "points_deducted": record.points_deducted,
        "quantity": record.quantity,
        "exchange_code": record.exchange_code,
        "exchange_time": record.exchange_time,
        "status": record.status,
        "validity_start_date": record.validity_start_date,
        "validity_end_date": record.validity_end_date
    }
