from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "scraper.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

Base = declarative_base()

class ScrapedItem(Base):
    __tablename__ = "scraped_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    currency = Column(String)
    url = Column(String)
    source_type = Column(String) # 'static' or 'dynamic'
    scraped_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_items(items):
    db = SessionLocal()
    try:
        for item in items:
            db_item = ScrapedItem(**item)
            db.add(db_item)
        db.commit()
        return len(items)
    except Exception as e:
        db.rollback()
        print(f"Error saving items: {e}")
        return 0
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
