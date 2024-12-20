import sys
sys.path.append( "..")
import models
from database import get_db
from fastapi import Depends,HTTPException,status,APIRouter,Header,File, UploadFile
from schemas import course_data,update_course_data,course_advisor,course_batches
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from io import BytesIO
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import os
from starlette.responses import FileResponse
from datetime import datetime
# from typing import Optional


router = APIRouter(
    prefix="/home",
    tags=["home"],
    responses={401:{"user":"testing purpose"}}
)

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    try:
        new=db.query(models.Users).all()
        return {"sucess":True,"message":new}
    except Exception as e:
        return {"success":False,"message":str(e)}
@router.post("/user_creation")
def update_user_type(db: Session = Depends(get_db)):
    user_model = models.Users()
    user_model.Name = "suadmin"
    user_model.email = "suadmin@local.in"
    user_model.password = "Welcome@123"
    user_model.User_type = "super_user"
    user_model.status = True 
    db.add(user_model)
    db.commit()
    return {"message": "User type updated successfully", "user": user_model.email}



UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True) 


#####this api for all file uplaod method ###
"""
adds image and return the path
Args :
file:attach file path and saving data 
return:return the file path in dict"""

@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # existing_image = db.query(Image).filter(Image.file_path == file.filename).first()
        # if existing_image:
        #     return {
        #         "message": "Duplicate filename detected",
        #         "image_id": existing_image.id,
        #         "file_url": f"/files/{existing_image.file_path}",
        #     }

        # Save the file with the original filename
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        if os.path.exists(file_path):
            return {"success":False,"message":"File already exists","file_url":f"/files/{file.filename}"}
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        return {
            "success":True,
            "message": "File uploaded successfully",
            "file_url": f"/files/{file.filename}",
        }
    except Exception as e:
        return {"success":False,"message":str(e)}


####this api for adding course data ####
"""Adds a course with details and uploads associated images.
    Args:
        course (CourseData): Course metadata.
        db (Session): Database session.
    Returns:
        dict: Response with success status and uploaded file URLs.
    """
@router.post("/add_course")
async def upload_course(course: course_data,db: Session = Depends(get_db)):
    try:
        new_course = models.Course()
        new_course.title = course.title
        new_course.description = course.description
        new_course.duration = course.duration
        new_course.upcoming_batch = course.upcoming_batch
        new_course.bg_img = course.bg_img
        new_course.course_img = course.course_img
        new_course.course_fee = course.course_fee
        new_course.eligibility = course.eligibility
        new_course.route = course.route
        db.add(new_course)
        db.commit()

        return {
                "success": True,
                "message":"Course added sucessfully"
            }
    except Exception as e:
      return{"success":False,"message":"Duplicate form fields","error":str(e)}
    
###this api get the all course_data ####
"""
args:no arguments getting all course data
Returns:dict: Response with success status and get the all course columns data."""
@router.get("/all_course_data")
async def all_get_course_data(db: Session = Depends(get_db)):
    try:
        all_data = db.query(models.Course).order_by(models.Course.id.asc()).all()
        result = []
        for course in all_data:
           course_dict = course.__dict__.copy()
        #    course_dict["duration"] = f"{course.duration} Months"
           course_dict["upcoming_batch_name"] = course.upcoming_batch.strftime("%d %b %Y")
        #    course_dict["course_fee"] = f"INR {course.course_fee:,.0f} + GST"
           result.append(course_dict)
        return{"success":True,"message":result}
    except Exception as e:
        return{"success":False,"message":"Getting error data","error":str(e)}
    
#### in this api update and delete for the course data #####
"""args:update_course_data metadata,
id :when update are delete couse id data
db (Session): Database session.
return: Response with success status update are deleted """
@router.put("/update_course_data/{id}")
async def update_and_delete_course_data(id:int,update:update_course_data,db: Session = Depends(get_db)):
    try:
        update_course = db.query(models.Course).filter(models.Course.id==id).first()
        if  update_course:
            if update.action == True:
                update_course.title = update.title
                update_course.description = update.description
                update_course.duration = update.duration
                update_course.upcoming_batch = update.upcoming_batch
                update_course.bg_img = update.bg_img
                update_course.course_img = update.course_img
                update_course.course_fee = update.course_fee
                update_course.eligibility = update.eligibility
                update_course.route = update.route
                db.add(update_course)
                db.commit()
                return {"success":True,"message":"Updated successfully"}
            elif update.action == False:
                db.delete(update_course)
                db.commit()
                return{"success":True,"message":"Course deleted successfully"}  
        else:
            return{"success":False,"message":"No courses found"} 
    except Exception as e:
        return{"success":False,"message":"Duplicate form fields","error":str(e)}
    


#### in this api we collecting students data for which course they interest ##### 
"""Adds a students data with details .
    Args:
        course_student (student Data): Course Student metadata.
        db (Session): Database session.
    Returns:
        dict: Response with success status .
    """

@router.post("/add_student_data")
async def creating_student_data(course_student: course_advisor,db: Session = Depends(get_db)):
    try:
        get_student_data = db.query(models.course_advisor).filter(models.course_advisor.email==course_student.email,models.course_advisor.course_type==course_student.course_type).first()
        if get_student_data:
          return {"success":False,"message":"Email Already Exists"}
        student_data = models.course_advisor()
        student_data.course_type = course_student.course_type
        student_data.first_name = course_student.first_name
        student_data.last_name = course_student.last_name
        student_data.email = course_student.email
        student_data.mobile_number = course_student.mobile_number
        student_data.qualification = course_student.qualification
        student_data.gender = course_student.gender
        db.add(student_data)
        db.commit()
        return {"success": True,"message":"Contacted sucessfully"}
    except Exception as e:
      return{"success":False,"message":"Email already exists","error":str(e)}
    
####  Upcoming Course Dates & Batches   ###
"""Adds a upcoming course dates & batches details .
    Args:
        course_batches (batches data): Course Batches metadata.
        db (Session): Database session.
    Returns:
        dict: Response with success status .
    """
@router.post("/add_upcoming_batch")
async def creating_upcoming_batch_data(upcoming_data: course_batches,db: Session = Depends(get_db)):
    try:
        batches_data = models.course_batches()
        batches_data.course_type = upcoming_data.course_type
        batches_data.from_batch = upcoming_data.from_batch
        batches_data.duration = upcoming_data.duration
        batches_data.days = upcoming_data.days
        batches_data.training_type = upcoming_data.training_type
        batches_data.timings = upcoming_data.timings
        batches_data.location = upcoming_data.location
        batches_data.course_fee = upcoming_data.course_fee
        batches_data.vacancies = upcoming_data.vacancies
        db.add(batches_data)
        db.commit()
        return {"success": True,"message":"Batch created sucessfully"}
    except Exception as e:
      return{"success":False,"message":"Creation Problem","error":str(e)}
    
###this api get the course wise batch data ####
"""
args:
batch_data:batch_data(metadata)
Returns:dict: Response with success status and get the all course wise batch data."""
@router.get("/all_batches_data")
async def course_type_batch_data(course_type: str,db: Session = Depends(get_db)):
    try:
        all_data = db.query(models.course_batches).filter(models.course_batches.course_type == course_type).order_by(models.course_batches.updated_at.asc()).all()

        result = []
        for course in all_data:
            course_dict = course.__dict__.copy()
            course_dict["next_batch_name"] = course.from_batch.strftime("%b %d ,%Y")
            result.append(course_dict)
        
        return {"success": True, "message": result}
    except Exception as e:
        return {"success": False, "message": "Getting error data", "error": str(e)}

