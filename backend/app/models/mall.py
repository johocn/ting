from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database import Base

class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("product_categories.id"))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("product_categories.id"))
    points_required = Column(Integer, nullable=False)  # 所需积分
    stock_quantity = Column(Integer, default=0)  # 库存数量
    max_exchange_per_user = Column(Integer, default=0)  # 单用户最大兑换次数
    is_active = Column(Boolean, default=True)
    is_virtual = Column(Boolean, default=False)  # 是否为虚拟商品
    validity_period_days = Column(Integer)  # 有效期天数（虚拟商品）
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExchangeRecord(Base):
    __tablename__ = "exchange_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    points_deducted = Column(Integer, nullable=False)  # 扣除积分
    quantity = Column(Integer, default=1)  # 兑换数量
    exchange_code = Column(String(50), unique=True)  # 兑换码
    exchange_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='pending')  # pending, confirmed, used, cancelled
    validity_start_date = Column(DateTime)  # 有效期开始
    validity_end_date = Column(DateTime)  # 有效期结束
    created_at = Column(DateTime, default=datetime.utcnow)

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    manager_user_id = Column(Integer, ForeignKey("users.id"))  # 门店管理员
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class VerificationRecord(Base):
    __tablename__ = "verification_records"

    id = Column(Integer, primary_key=True, index=True)
    exchange_record_id = Column(Integer, ForeignKey("exchange_records.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))
    verifier_user_id = Column(Integer, ForeignKey("users.id"))  # 核销员
    verification_time = Column(DateTime, default=datetime.utcnow)
    verification_code = Column(String(50))  # 核销码
    status = Column(String(20), default='verified')  # verified, cancelled
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class StoreEmployee(Base):
    __tablename__ = "store_employees"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(50), default='employee')  # employee, manager
    is_active = Column(Boolean, default=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)

class VerificationPermission(Base):
    __tablename__ = "verification_permissions"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    can_verify = Column(Boolean, default=True)
    can_cancel = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('store_id', 'user_id'),)
