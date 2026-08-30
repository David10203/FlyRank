from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


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

    new_task = {
        "id": next_id,
        "title": task_data.title,
        "done": False
    }

    tasks.append(new_task)
    next_id += 1

    return new_task
