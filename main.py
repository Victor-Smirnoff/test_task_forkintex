import uvicorn
from fastapi import FastAPI
import asyncio
from time import monotonic
from pydantic import BaseModel

app = FastAPI()
lock = asyncio.Lock()


async def work() -> None:
    await asyncio.sleep(3)


class TestResponse(BaseModel):
    elapsed: float


@app.get("/test", response_model=TestResponse)
async def handler() -> TestResponse:
    ts1 = monotonic()

    async with lock:
        await work()

    ts2 = monotonic()
    elapsed = ts2 - ts1

    return TestResponse(elapsed=elapsed)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
