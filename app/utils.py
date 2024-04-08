from .schemas import (
    StudentCreate,
    SingleStudentSearchResponse,
    StudentUpdate,
)
from pymongo.database import Database
from bson.objectid import ObjectId


async def add_student(student: StudentCreate, db: Database):
    try:
        student_data = student.model_dump()
        result = db.students.insert_one(student_data)
        if result.acknowledged:
            return {"status": True, "data": {"id": str(result.inserted_id)}}
        else:
            return {"status": False}
    finally:
        await db.client.close()


async def search_students(db: Database, country: str = None, age: int = None):
    try:
        query = {}
        if country:
            query["address.country"] = country
        if age is not None:
            query["age"] = {"$gte": age}
        result = db.students.find(query)
        data = [student for student in result]
        return {"data": data, "status": True}
    except Exception as e:
        return {"status": False}
    finally:
        await db.client.close()


async def search_students_by_id(student_id: str, db: Database):
    try:
        result = db.students.find_one({"_id": ObjectId(student_id)})
        if result:
            result["id"] = result["_id"]
            return {"status": True, "data": SingleStudentSearchResponse(**result)}
        else:
            return {"status": False}
    except Exception as e:
        return {"status": False}
    finally:
        await db.client.close()


async def update_by_id(student_id: str, student: StudentUpdate, db: Database):
    try:
        update_data = student.model_dump(exclude_unset=True)
        update_query = {}
        update_query["$set"] = update_data

        if update_query:
            result = db.students.update_one({"_id": ObjectId(student_id)}, update_query)
            if result.modified_count > 0:
                return {"status": True}
        else:
            return {"status": False, "detail": "No valid fields to update"}
    except Exception as e:
        return {"status": False}
    finally:
        await db.client.close()


async def delete_by_id(student_id: str, db: Database):
    try:
        result = db.students.delete_one({"_id": ObjectId(student_id)})
        if result.deleted_count > 0:
            return {"status": True}
        else:
            return {"status": False}
    except Exception as e:
        return {"status": False}
    finally:
        await db.client.close()
