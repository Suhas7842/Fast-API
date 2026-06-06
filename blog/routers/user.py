from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..hashing import Hash
from .. import schemas, database
from ..repository import user

router = APIRouter(
    prefix="/api",
    tags=["Users"]
)

@router.post('/',response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create_user(request, db)

@router.get('/{id}', response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    return user.get_user_by_id(id, db)