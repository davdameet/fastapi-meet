from fastapi import status,HTTPException, Depends,APIRouter
from .. import schemas,database,oauth,models
from sqlalchemy.orm import Session
router=APIRouter()
@router.post("/votes")
def vote(vote:schemas.vote,db:Session =Depends(database.get_db),user_id:int= Depends(oauth.get_currentUser)):
    post=db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if(not post):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The post with this id was not found")
    vote_query=db.query(models.votes).filter(models.votes.posts_id == vote.post_id, models.votes.users_id == user_id.id)
    found_post=vote_query.first()
    if(vote.dir ==1):
        if found_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="You cannot like the same post again and again")
        new_vote=models.votes(posts_id=vote.post_id,users_id=user_id.id)
        db.add(new_vote)
        db.commit()
        return{"message":"successfully created vote"}
    else:
        if not found_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"successfully deleted vote"} 
