from fastapi import FastAPI, status, HTTPException, Depends, Query, Path

from . import schemas, utils
from .database import get_db
from typing import Optional

from pymongo.database import Database

app = FastAPI(
    title="Backend Intern Hiring Task",
    description="You have to implement these APIs in FastAPI and MongoDB tech stack as mentioned on your problem statement document.",
)


@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.StudentCreateResponse,
    description="API to create a student in the system. All fields are mandatory and required while creating the student in the system.",
)
async def creates_students(
    student: schemas.StudentCreate, db: Database = Depends(get_db)
):
    try:
        result = await utils.add_student(student, db)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["detail"],
            )
        else:
            return result["data"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.get(
    "/students",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    description="An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.",
)
async def list_students(
    country: str = Query(
        None,
        description="To apply filter of country. If not given or empty, this filter should be applied.",
    ),
    age: int = Query(
        None,
        description="Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied.",
    ),
    db: Database = Depends(get_db),
):
    try:
        result = await utils.search_students(db, country, age)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["detail"],
            )
        else:
            return {"data": result["data"]}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.get(
    "/students/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.SingleStudentSearchResponse,
    description="API to retrieve information about a specific student by their ID.",
)
async def fetch_student(
    id: str = Path(..., description="The ID of the student previously created."),
    db: Database = Depends(get_db),
):
    try:
        result = await utils.search_students_by_id(id, db)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["detail"],
            )
        else:
            return result["data"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.patch(
    "/students/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.",
    summary="Update a student by ID",
)
async def update_student(
    id: str,
    student: Optional[schemas.StudentUpdate] = None,
    db: Database = Depends(get_db),
):
    try:
        result = await utils.update_by_id(id, student, db)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=result["detail"],
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.delete(
    "/students/{id}",
    status_code=status.HTTP_200_OK,
)
async def delete_student(id: str, db: Database = Depends(get_db)):
    try:
        result = await utils.delete_by_id(id, db)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["detail"],
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# @app.get("/app-check", status_code=status.HTTP_200_OK)
# async def app_check():
#     return {"message": "Hello Earth"}


# @app.get("/database-check", status_code=status.HTTP_200_OK)
# async def db_check(db: Database = Depends(get_db)):
#     try:
#         db.command("ping")
#         return {"message": "DB conected"}
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#             detail="Failed to connect to the database.",
#         )
