from fastapi import FastAPI

app = FastAPI()

@app.post("/")
def home():

    context = {
        'name': 'Krishna Regmi',
        'course': 'Computer Science'
    }

    return context