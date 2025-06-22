from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.database import crud
from src.schemas.user import UserCreate, UserInDB

router = APIRouter()


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user.user_id)
    if db_user:
        if db_user.design_id == user.design_id:
            raise HTTPException(status_code=400, detail="User already registered")
        else:
            print("updating design id")
            return crud.update_design_id(db=db, user=user)
    return crud.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=UserInDB)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    db_conext = crud.get_user_context(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
