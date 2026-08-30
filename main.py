from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str | None = None
    done: bool | None = None


tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build a Task API",
        "done": False
    },
    {
        "id": 3,
        "title": "Learn Git and GitHub",
        "done": False
    }
]

next_id = 4

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    global next_id

    if task_data.title is None or not task_data.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required and cannot be empty"
        )

    new_task = {
        "id": next_id,
        "title": task_data.title.strip(),
        "done": False
    }

    tasks.append(new_task)
    next_id += 1

    return new_task




@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskCreate):

    if task_data.title is None and task_data.done is None:
        raise HTTPException(
            status_code=400,
            detail="Request body must contain title or done"
        )

    if task_data.title is not None and not task_data.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    for task in tasks:
        if task["id"] == task_id:

            if task_data.title is not None:
                task["title"] = task_data.title.strip()

            if task_data.done is not None:
                task["done"] = task_data.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )