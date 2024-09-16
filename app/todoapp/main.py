from fastapi import FastAPI
from .database import engine
from .routers import auth, todos, admin, users
from . import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

@app.get('/health')
async def health_check():
    return {'message':'Server Running.'}