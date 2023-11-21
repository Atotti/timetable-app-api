from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Reactアプリのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

# 授業情報のモデル
class ClassInfo(BaseModel):
    id: int
    name: str
    day: int  # 曜日を整数で表現
    period: int  # 時限を整数で表現
    room: str

# 仮の授業データ
classes_data = [
    {"id": 1, "name": "数学入門1", "day": 1, "period": 1, "room": "101教室"},
    {"id": 2, "name": "数学入門2", "day": 1, "period": 1, "room": "101教室"},
    {"id": 3, "name": "数学入門3", "day": 1, "period": 1, "room": "101教室"},
    {"id": 4, "name": "数学入門4", "day": 1, "period": 1, "room": "101教室"},
    {"id": 5, "name": "数学入門5", "day": 1, "period": 1, "room": "101教室"},
    {"id": 6, "name": "物理学基礎", "day": 2, "period": 2, "room": "102教室"},
    # 他のデータ...
]

# 指定された曜日と時限に開講されている授業を取得するAPIエンドポイント
@app.get("/classes/{day}/{period}", response_model=List[ClassInfo])
async def get_classes_by_day_and_period(day: int, period: int):
    filtered_classes = [c for c in classes_data if c["day"] == day and c["period"] == period]
    return filtered_classes

# uvicorn main:app --reload