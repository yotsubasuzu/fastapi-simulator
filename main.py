import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from parser import process_log_line

app = FastAPI()


class LogLine(BaseModel):
    line: str


@app.post("/log")
def receive_log(log: LogLine):
    process_log_line(log.line)
    return {"message": "Log processed"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
