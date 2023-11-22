from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from pydantic import BaseModel

# データベース接続
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite3.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemyモデルの定義(ORMのモデル定義)
class SyllabusBaseInfoSplitedByDayAndPeriodJoinClassroomAllocation(Base):
    __tablename__ = "syllabus_base_info_splited_by_day_and_period_join_classroom_allocation"

    year = Column(Integer)
    season = Column(String)
    day = Column(String)
    period = Column(String)
    teacher = Column(String)
    name = Column(String)
    lecture_id = Column(String, primary_key=True, index=True)
    credits = Column(Integer)
    url = Column(String)
    type = Column(String)
    faculty = Column(String)
    campus = Column(String)
    building = Column(String)
    room_id = Column(String)

# db向けの曜日と時限のマッピング
day_map = {1:"月", 2:"火", 3:"水", 4:"木", 5:"金"}
period_map = {1:"1限", 2:"2限", 3:"3限", 4:"4限", 5:"5限", 6:"6限"}

# 依存性を使用してデータベースセッションを取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Reactアプリのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

# 授業情報のモデル(fastAPIのjsonの定義)
class ClassInfo(BaseModel):
    year: Optional[int]
    season: Optional[str]
    day: int
    period: int
    teacher: Optional[str]
    name: str
    lecture_id: str
    credits: Optional[int]
    url: Optional[str]
    type: Optional[str]
    faculty: Optional[str]
    campus: Optional[str]
    building: Optional[str]
    room_id: Optional[str]

# 戻り値向けマッピング
day_map2 = {"月":1, "火":2, "水":3, "木":4, "金":5}
period_map2 = {"1限":1, "2限":2, "3限":3, "4限":4, "5限":5, "6限":6}

def day_map2_func(x):
    x.day = day_map2[x.day]
    return x

def period_map2_func(x):
    x.period = period_map2[x.period]
    return x

# 指定された曜日と時限に開講されている授業を取得するAPIエンドポイント
@app.get("/classes/{day}/{period}", response_model=List[ClassInfo])
async def get_classes_by_day_and_period(day: int, period: int, db: Session = Depends(get_db)):
    filtered_classes = db.query(SyllabusBaseInfoSplitedByDayAndPeriodJoinClassroomAllocation).filter(SyllabusBaseInfoSplitedByDayAndPeriodJoinClassroomAllocation.day == day_map[day], SyllabusBaseInfoSplitedByDayAndPeriodJoinClassroomAllocation.period == period_map[period]).all()
    filtered_classes = list(map(day_map2_func, filtered_classes))
    filtered_classes = list(map(period_map2_func, filtered_classes))
    
    return filtered_classes

# uvicorn main:app --reload