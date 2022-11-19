from fastapi import FastAPI
from sqlalchemy import String, Column, Integer, Float, create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "sqlite:///./main.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False}, 
    echo=True
)

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    latitude = Column('latitude', Float) # 緯度
    longitude = Column('longitude', Float) # 経度
    imagepath = Column('imagepath', String, nullable=True) # 画像
    audiopath = Column('audiopath', String, nullable=True) # 音声のパス
    
if __name__ == '__main__':
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)