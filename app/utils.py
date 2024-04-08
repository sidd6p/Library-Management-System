from .schemas import (
    StudentCreate,
    SingleStudentSearchResponse,
    StudentUpdate,
    StudentBaseModel,
)
from pymongo.database import Database
from bson.objectid import ObjectId


async def add_student(student: StudentCreate, db: Database):
    student_data = student.model_dump()
    result = db.students.insert_one(student_data)
    if result.acknowledged:
        return {"status": 1, "data": {"id": str(result.inserted_id)}}
    else:
        return {"status": 0, "detail": "Operation success is uncertain"}


async def search_students(db: Database, country: str = None, age: int = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    result = db.students.find(query)
    print(result)
    data = [StudentBaseModel(**student) for student in result]
    print(result)
    if len(data) == 0:
        return {"status": 0, "detail": "No record found!"}

    return {"status": 1, "data": data}


async def search_students_by_id(student_id: str, db: Database):
    result = db.students.find_one({"_id": ObjectId(student_id)})
    if result:
        result["id"] = result["_id"]
        data = SingleStudentSearchResponse(**result)
        return {"status": 1, "data": data}
    else:
        return {"status": 0, "detail": "No record found!"}


async def update_by_id(student_id: str, student: StudentUpdate, db: Database):
    db_student = await search_students_by_id(student_id, db)
    print(db_student)
    if db_student["status"]:
        new_data = student.model_dump(exclude_unset=True)
        old_data = db_student["data"].model_dump()

        if "name" in new_data:
            old_data["name"] = new_data["name"]
        if "age" in new_data:
            old_data["age"] = new_data["age"]
        if "city" in new_data["address"]:
            old_data["address"]["city"] = new_data["address"]["city"]
        if "country" in new_data["address"]:
            old_data["address"]["country"] = new_data["address"]["country"]

        update_query = {"$set": old_data}
        if update_query["$set"]:
            result = db.students.update_one({"_id": ObjectId(student_id)}, update_query)
            if result.modified_count > 0:
                return {"status": 1}
            else:
                return {"status": 0, "detail": "No valid fields to update"}
    else:
        return {"status": 0, "detail": "No record found!"}


async def delete_by_id(student_id: str, db: Database):
    db_student = await search_students_by_id(student_id, db)
    if db_student["status"] == False:
        return {"status": 0, "detail": "No record found!"}
    else:
        db.students.delete_one({"_id": ObjectId(student_id)})
        return {"status": 1}
