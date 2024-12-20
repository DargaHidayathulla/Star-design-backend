from sqlalchemy import Boolean,Column,Integer,String,DateTime,func,Boolean,LargeBinary,Date,func,Time
from database import Base
from sqlalchemy.dialects.postgresql import BYTEA


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    User_type = Column(String)
    status = Column(Boolean, default=True)


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=True)  
    duration = Column(String(200), nullable=False)  
    upcoming_batch = Column(Date, nullable=False)  
    bg_img = Column(String(2083), nullable=True, index=True)
    course_img = Column(String(2083), nullable=True, index=True)
    course_fee = Column(Integer, nullable=False)  
    eligibility =  Column(String(500), nullable=True)
    route = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())  
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())



class course_advisor(Base):
    __tablename__ = "course_advisor"
    id =  Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_type = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    mobile_number = Column(String)
    qualification = Column(String)
    gender = Column(String)
    created_at = Column(DateTime, server_default=func.now())  
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class course_batches(Base):
    __tablename__ = "course_batches"
    id =  Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_type = Column(String)
    from_batch = Column(Date, nullable=False)
    duration = Column(String)
    days = Column(String)
    training_type =Column(String)
    timings = Column(String)
    location = Column(String)
    course_fee = Column(Integer, nullable=False)
    vacancies = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())  
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now()) 


