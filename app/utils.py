from .schemas import StudentSearchResponse


def search_students(country, age):
    dummy_data = [
        {"name": "John", "age": 20},
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]
    return [StudentSearchResponse(**student) for student in dummy_data]
