from ..import schemas,models,utils
from fastapi import status,HTTPException, Depends,APIRouter
from .. database import get_db
from sqlalchemy.orm import Session
router=APIRouter()
@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseUser)
def createUsers(users:schemas.createUser,db: Session = Depends(get_db)):
    print(users.email)
    print(users.password)
    hashed_password=utils.hash(users.password)
    users.password=hashed_password
    new_user=models.users(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user
@router.get("/users/{id}",response_model=schemas.ResponseUser)
def get_user(id:int,db: Session = Depends(get_db)):
    single_user=db.query(models.users).filter(models.users.id == id).first()
    if not single_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The user with id:{id} does not exist")
    return single_user
