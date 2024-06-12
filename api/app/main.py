from fastapi import FastAPI

app = FastAPI(root_path="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the api! Make sure to take a look at the docs at /docs."}