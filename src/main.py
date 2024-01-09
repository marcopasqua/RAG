from pathlib import Path
from typing import Union

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from routes import file, chat


app = FastAPI()

app.include_router(file.router)
app.include_router(chat.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)