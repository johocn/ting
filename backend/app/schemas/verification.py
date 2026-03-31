from pydantic import BaseModel
from typing import Optional

class VerificationRequest(BaseModel):
    exchange_record_id: int
    verification_code: Optional[str] = ""

class VerificationResponse(BaseModel):
    status: str
    message: str

class StoreInfoResponse(BaseModel):
    store: dict

class VerificationStatsResponse(BaseModel):
    today_count: int
    month_count: int

class VerificationDetailResponse(BaseModel):
    detail: dict

class RecentVerificationsResponse(BaseModel):
    records: list

class QRCodeResponse(BaseModel):
    qr_code: str
