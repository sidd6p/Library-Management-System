from .schemas import StudentsSearchResponse


def search_students(country, age):
    dummy_data = [
        {"name": "John", "age": 20},
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]
    return {
        "data": [StudentsSearchResponse(**student) for student in dummy_data],
        "status": True,
    }


def search_students_by_id(id):
    dummy_data = {
        "name": "Siddhartha",
        "age": 25,
        "address": {"city": "Jalaun", "country": "India"},
    }
    return {"data": dummy_data, "status": True}


def add_student(student):
    dummy_data = {"id": "123"}
    return {"data": dummy_data, "status": True}


def update_by_id(id, student):
    return {"status": True}


def delete_by_id(id):
    return {"status": True}
