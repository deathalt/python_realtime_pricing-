from typing import Callable
import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from generate_values import run_generator, create_items_list

from settings import SERVER_PORT

app = FastAPI()
items_dict = run_generator()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_items/")
def collect_items() -> list[str]:
    return create_items_list()


@app.get("/")
def read_root(request: Request) -> Callable:
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/{item}/")
async def websocket_endpoint(websocket: WebSocket, item: str) -> None:
    index = int(item.split("_")[1])
    value = items_dict[index][item][0]
    await websocket.accept()
    for each_value in items_dict[index][item]:  # push init data to chart
        payload = {"value": each_value}
        await websocket.send_json(payload)
    while True:
        await asyncio.sleep(1)
        value = items_dict[index][item][-1]
        payload = {"value": value}
        await websocket.send_json(payload)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=SERVER_PORT, log_level="info")
