from .schemas import StudentsSearchResponse


def search_students(country, age):
    dummy_data = [
        {"name": "John", "age": 20},
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]
    return [StudentsSearchResponse(**student) for student in dummy_data]


def search_students_by_id(id):
    dummy_data = {
        "name": "Siddhartha",
        "age": 25,
        "address": {"city": "Jalaun", "country": "India"},
    }
    return dummy_data
