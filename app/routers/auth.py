from fastapi import status,HTTPException, Depends,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,models,utils,oauth
router=APIRouter()
@router.post("/login")
def login(var:OAuth2PasswordRequestForm = Depends(),db:Session =Depends(database.get_db)):
    login_user=db.query(models.users).filter(models.users.email == var.username).first()
    if not login_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
    if not utils.verify(var.password,login_user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    token=oauth.create_token(data={"user_id":login_user.id})
    return {"access_token":token,"token_type":"bearer"} 
    
