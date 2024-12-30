from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from .schemas import Blog
from . import models
from .db import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/blog", status_code=201)
def create_blog(request : Blog, db : Session = Depends(get_db)):
   new_blog = models.Blog(title=request.title, body=request.body)
   db.add(new_blog)
   db.commit()
   db.refresh(new_blog)
   return new_blog


@app.get("/blog", status_code=200)
def get_all_blogs(response : Response, db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if len(blogs) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"details":"No Blogs are present at the moment"}
    return blogs

@app.get("/blog/{id}", status_code=200)
def get_blog(id, response : Response, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} not found")
    return blog


@app.delete("/blog/{id}")
def delete_blog(id, db : Session = Depends(get_db)):
   db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
   db.commit()
   return {"details": f"Delete operation completed"}


@app.put("/blog/{id}")
def update_blog(id, request : Blog, db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update({"title" : request.title, "body" : request.body}, synchronize_session=False)
    db.commit()
    return {"details" : f"Update Operation Completed"}