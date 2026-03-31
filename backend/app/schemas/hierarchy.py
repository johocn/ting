from pydantic import BaseModel
from typing import List, Optional

class HierarchyPermission(BaseModel):
    code: str
    name: str
    enabled: bool

class HierarchyPointConfig(BaseModel):
    type: str
    multiplier: float
    fixed_bonus: int

class HierarchySubordinate(BaseModel):
    id: int
    name: str
    user_count: int
    commission_rate: float

class HierarchyUser(BaseModel):
    id: int
    username: str
    points: int
    is_active: bool

class HierarchyLevel(BaseModel):
    id: int
    name: str
    child_count: int
    total_users: int

class HierarchyLevelResponse(BaseModel):
    level: HierarchyLevel
    permissions: List[HierarchyPermission]
    point_configs: List[HierarchyPointConfig]
    subordinates: List[HierarchySubordinate]
    users: List[HierarchyUser]

class HierarchyStatisticsResponse(BaseModel):
    users: dict
    points: dict
    transactions: dict

class HierarchySubordinatesResponse(BaseModel):
    subordinates: List[dict]

class HierarchyUsersResponse(BaseModel):
    users: List[dict]
