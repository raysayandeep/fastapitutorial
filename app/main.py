from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional

app = FastAPI()

var_post = []

class post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

    @field_validator('rating')
    def rating_not_gt_5(rating):
        if rating > 5:
            raise ValueError('Rating should not be more than 5')
        else:
            return rating

@app.get("/")
def main():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "This is an example post"}


@app.post("/createposts")
def create_posts(new_post: post):
    print(new_post.published,new_post.rating)
    print(new_post.model_dump())
    var_post = new_post
    #return {"title": "new data"}
    return {"data":var_post}

