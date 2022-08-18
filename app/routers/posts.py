from ..import schemas,models,oauth
from fastapi import status,HTTPException, Depends,APIRouter
from .. database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
router=APIRouter()
@router.get("/posts",response_model=List[schemas.Response_post]) 
def get_posts(db: Session = Depends(get_db),search:Optional[str]=""):
    # cursor.execute(''' SELECT * FROM posts''')
    # posts=cursor.fetchall()
    # print(posts)
    all_posts=db.query(models.Post).filter(models.Post.title.contains(search)).all()
    return  all_posts
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Response_post)
def create_posts(var:schemas.Post,db: Session = Depends(get_db),user_id:int= Depends(oauth.get_currentUser)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) returning *""",(var.title,var.content,var.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(user_id=user_id.id,**var.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post
@router.get("/posts/{id}")
def get_post(id:int,db: Session = Depends(get_db),user_id:int= Depends(oauth.get_currentUser)):
    # cursor.execute(""" SELECT * FROM  posts WHERE id = %s """,(str(id),)) 
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} was not found!")
    return {"post Details ": post}
@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),user_id:int= Depends(oauth.get_currentUser)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    # deletedPost=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if(post == None):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"There was no post related to id:{id}")
    print(type(user_id.id))
    if(post.user_id != user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cannot delete other person's posts")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"the deleted post":post}
@router.put("/posts/{id}")
def update_post(id:int,Post:schemas.Post,db: Session = Depends(get_db),user_id:int= Depends(oauth.get_currentUser)):
    # cursor.execute(""" UPDATE posts SET title = %s , content = %s, published =%s WHERE id = %s""",(Post.title,Post.content,Post.published,str(id)),)
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if(not post):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"The post with id : {id} not found !")
    if(post.user_id != user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cannot update any other person's post")
    post_query.update(Post.dict(),synchronize_session=False)
    db.commit()
    return "data updated successfully!"