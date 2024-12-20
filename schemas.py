from pydantic import BaseModel
# from database import SessionLocal,engine
# from fastapi import Depends,HTTPException,status,APIRouter,Header,File, UploadFile
class course_data(BaseModel):
    title:str
    description :str
    duration :str
    upcoming_batch :str
    bg_img:str
    course_img:str
    course_fee:int
    eligibility:str
    route:str

class update_course_data(BaseModel):
    title:str
    description :str
    duration :str
    upcoming_batch :str
    bg_img:str
    course_img:str
    course_fee:int
    eligibility:str
    action: bool
    route:str 

class course_advisor(BaseModel):
    course_type :str
    first_name :str
    last_name:str
    email:str
    mobile_number:str
    qualification:str
    gender:str

class course_batches(BaseModel):
    course_type :str
    from_batch :str
    duration:str
    days:str
    training_type:str
    timings:str
    location:str
    course_fee:int
    vacancies:int
