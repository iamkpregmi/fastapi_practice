from pydantic import BaseModel

class TestBase(BaseModel):
    name: str

class TestCreate(TestBase):
    pass

class TestResponse(TestBase):
    id: int

    class Config:
        orm_mode = True
