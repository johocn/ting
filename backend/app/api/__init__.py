from fastapi import APIRouter
from app.api import auth, users, contents, quizzes, points, channels, hierarchy, verification, learning_progress, mall
from app.api.sign_notifications import sign_notifications_router
from app.api.analytics import analytics_router

router = APIRouter()

# 注册所有API路由
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(contents.router, prefix="/contents", tags=["contents"])
router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
router.include_router(points.router, prefix="/points", tags=["points"])
router.include_router(channels.router, prefix="/channels", tags=["channels"])
router.include_router(hierarchy.router, prefix="/hierarchy", tags=["hierarchy"])
router.include_router(verification.router, prefix="/verification", tags=["verification"])
router.include_router(learning_progress.router, prefix="/learning", tags=["learning"])
router.include_router(sign_notifications_router, prefix="/sign", tags=["sign"])
router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
router.include_router(mall.router, prefix="/mall", tags=["mall"])
