import uvicorn
import logging
from enum import Enum
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StatusEnum(str, Enum):
    done = "выполнена"
    not_done = "не выполнена"

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum

tasks = [
    Task(
        id=1,
        title="Learn Fastapi",
        description="try to learn Fastapi",
        status=StatusEnum.not_done,
    ),
    Task(
        id=2,
        title="Homework 5",
        description="send to GB",
        status=StatusEnum.done,
    ),
]

@app.get("/tasks", response_model=List[Task])
async def get_tasks(task_id: Optional[int] = None):
    if task_id is not None:
        task = next((task for task in tasks if task.id == task_id), None)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return [task]
    return tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    if any(t.id == task.id for t in tasks):
        raise HTTPException(status_code=403, detail="This id is already in use")
    tasks.append(task)
    logger.info(f"Task id={task.id} {task.title} - успешно добавлен")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i] = task
            logger.info(f"Task id={task.id} - успешно изменен")
            return tasks[i]
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[i]
            logger.info(f"Task id={task.id} {task.title} - успешно удален")
            return {"message": f"Task id={task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/status", response_model=List[Task])
async def get_tasks_by_status(status: StatusEnum = Query(...)):
    return [task for task in tasks if task.status == status]

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)