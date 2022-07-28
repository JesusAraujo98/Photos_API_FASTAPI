from fastapi import FastAPI
from .users.routes import users
from .albums.routes import albums

app = FastAPI()

app.include_router(users)
app.include_router(albums)



