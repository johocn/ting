from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.models import Product, ProductCategory, Content, User
from app.core.config import settings

# 创建数据库引擎
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    db = SessionLocal()
    
    try:
        # 添加商品类别
        categories = [
            {"name": "实体商品", "description": "实物商品"},
            {"name": "虚拟商品", "description": "在线服务或虚拟物品"},
            {"name": "优惠券", "description": "折扣或优惠券"},
            {"name": "学习资料", "description": "电子书或学习材料"}
        ]
        
        for cat_data in categories:
            existing_cat = db.query(ProductCategory).filter(ProductCategory.name == cat_data["name"]).first()
            if not existing_cat:
                category = ProductCategory(**cat_data)
                db.add(category)
        
        db.commit()
        
        # 获取类别ID
        physical_cat = db.query(ProductCategory).filter(ProductCategory.name == "实体商品").first()
        virtual_cat = db.query(ProductCategory).filter(ProductCategory.name == "虚拟商品").first()
        voucher_cat = db.query(ProductCategory).filter(ProductCategory.name == "优惠券").first()
        study_cat = db.query(ProductCategory).filter(ProductCategory.name == "学习资料").first()
        
        # 添加商品
        products = [
            {
                "name": "精美笔记本",
                "description": "高品质笔记本，适合学习记录",
                "category_id": physical_cat.id if physical_cat else 1,
                "points_required": 500,
                "stock_quantity": 100,
                "max_exchange_per_user": 1,
                "is_virtual": False,
                "validity_period_days": 0
            },
            {
                "name": "学习视频会员",
                "description": "一个月学习视频会员",
                "category_id": virtual_cat.id if virtual_cat else 2,
                "points_required": 800,
                "stock_quantity": 500,
                "max_exchange_per_user": 1,
                "is_virtual": True,
                "validity_period_days": 30
            },
            {
                "name": "T恤衫",
                "description": "舒适棉质T恤，多种颜色可选",
                "category_id": physical_cat.id if physical_cat else 1,
                "points_required": 1200,
                "stock_quantity": 30,
                "max_exchange_per_user": 1,
                "is_virtual": False,
                "validity_period_days": 0
            },
            {
                "name": "积分翻倍卡",
                "description": "使用后下次学习积分翻倍",
                "category_id": virtual_cat.id if virtual_cat else 2,
                "points_required": 300,
                "stock_quantity": 200,
                "max_exchange_per_user": 3,
                "is_virtual": True,
                "validity_period_days": 7
            },
            {
                "name": "优惠券",
                "description": "10元现金优惠券",
                "category_id": voucher_cat.id if voucher_cat else 3,
                "points_required": 1000,
                "stock_quantity": 80,
                "max_exchange_per_user": 2,
                "is_virtual": False,
                "validity_period_days": 30
            },
            {
                "name": "精美水杯",
                "description": "保温水杯，陪伴你的学习时光",
                "category_id": physical_cat.id if physical_cat else 1,
                "points_required": 600,
                "stock_quantity": 60,
                "max_exchange_per_user": 1,
                "is_virtual": False,
                "validity_period_days": 0
            },
            {
                "name": "Python编程入门",
                "description": "Python编程基础电子书",
                "category_id": study_cat.id if study_cat else 4,
                "points_required": 300,
                "stock_quantity": 1000,
                "max_exchange_per_user": 1,
                "is_virtual": True,
                "validity_period_days": 0
            },
            {
                "name": "英语学习套餐",
                "description": "英语学习视频套餐",
                "category_id": virtual_cat.id if virtual_cat else 2,
                "points_required": 1500,
                "stock_quantity": 50,
                "max_exchange_per_user": 1,
                "is_virtual": True,
                "validity_period_days": 365
            }
        ]
        
        for product_data in products:
            existing_product = db.query(Product).filter(Product.name == product_data["name"]).first()
            if not existing_product:
                product = Product(**product_data)
                db.add(product)
        
        db.commit()
        
        # 添加学习内容
        contents = [
            {
                "title": "JavaScript基础教程",
                "url": "https://example.com/js-basics.mp4",
                "duration": 1800,
                "category": "编程",
                "description": "JavaScript编程语言基础知识讲解",
                "reward_points_per_minute": 5,
                "status": True
            },
            {
                "title": "Python进阶课程",
                "url": "https://example.com/python-advanced.mp4",
                "duration": 2700,
                "category": "编程",
                "description": "Python高级编程技巧和最佳实践",
                "reward_points_per_minute": 6,
                "status": True
            },
            {
                "title": "Vue.js实战",
                "url": "https://example.com/vue-practice.mp4",
                "duration": 2400,
                "category": "前端",
                "description": "Vue.js框架实战开发项目",
                "reward_points_per_minute": 5,
                "status": True
            },
            {
                "title": "Node.js入门",
                "url": "https://example.com/node-intro.mp4",
                "duration": 1800,
                "category": "后端",
                "description": "Node.js服务端开发入门教程",
                "reward_points_per_minute": 5,
                "status": True
            },
            {
                "title": "React基础教程",
                "url": "https://example.com/react-basics.mp4",
                "duration": 2100,
                "category": "前端",
                "description": "React框架基础概念和使用方法",
                "reward_points_per_minute": 5,
                "status": True
            },
            {
                "title": "算法与数据结构",
                "url": "https://example.com/algorithms.mp4",
                "duration": 3000,
                "category": "算法",
                "description": "常见算法和数据结构讲解",
                "reward_points_per_minute": 6,
                "status": True
            },
            {
                "title": "CSS布局技巧",
                "url": "https://example.com/css-layout.mp4",
                "duration": 1500,
                "category": "前端",
                "description": "CSS布局的各种技巧和最佳实践",
                "reward_points_per_minute": 4,
                "status": True
            },
            {
                "title": "数据库设计原理",
                "url": "https://example.com/db-design.mp4",
                "duration": 2400,
                "category": "后端",
                "description": "数据库设计的基本原理和实践",
                "reward_points_per_minute": 6,
                "status": True
            }
        ]
        
        from app.models.contents import Content as ContentModel
        
        for content_data in contents:
            existing_content = db.query(ContentModel).filter(ContentModel.title == content_data["title"]).first()
            if not existing_content:
                content = ContentModel(**content_data)
                db.add(content)
        
        db.commit()
        print("数据填充完成!")
        
    except Exception as e:
        print(f"数据填充失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()