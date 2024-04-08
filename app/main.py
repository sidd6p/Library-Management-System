from fastapi import FastAPI, status


app = FastAPI()


@app.get("/students", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello Earth"}


@app.get("/students{id}", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello Earth"}


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def root():
    return {"message": "Hello Earth"}


@app.patch("/students{id}", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello Earth"}


@app.delete("/students{id}", status_code=status.HTTP_204_NO_CONTENT)
async def root():
    return {"message": "Hello Earth"}
