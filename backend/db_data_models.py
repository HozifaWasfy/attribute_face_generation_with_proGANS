from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db_engine import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,autoincrement=True ,  primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    content_directory = Column(String)

    images = relationship("Images", back_populates="owner")


class Images(Base):
    __tablename__ = "generated_images"

    id = Column(Integer, autoincrement= True, primary_key=True, index=True)
    name = Column(String, index=True)
    num_faces = Column(Integer)
    noise = Column(String)
    attributes = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="images")
    
# User.__table__.create(engine)
# Images.__table__.create(engine)
    