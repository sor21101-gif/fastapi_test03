# database.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# db접속 정보
DB_URL = "postgresql://scott:tiger@172.16.8.101/scott_db"
# db엔진 만들기
engine = create_engine(DB_URL)
# 세션 만들기
SesstionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 글 목록기능(post)
CREATE_POST_TABLE = """
    CREATE TABLE IF NOT EXISTS post(
        num SERIAL PRIMARY KEY,
        writer VARCHAR(50) NOT NULL,
        title VARCHAR(100),
        content TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    )
"""
# db연결시 테이블이 없으면 만들기
with engine.connect() as connection:
    connection.execute(text(CREATE_POST_TABLE))
    connection.commit()

# db객체를 리턴해주는 함수(main.py등에서 import해서 사용할 예정)
def get_db():
    db = SesstionLocal()
    try:
        yield db
    finally:
        db.close()