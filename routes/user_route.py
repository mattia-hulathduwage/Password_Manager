from fastapi import Depends, APIRouter
from schemas.user_schema import User, Login
import database.database_model as data
from dependency import get_db
from sqlalchemy.orm import Session
from auth import hash_password, verify_password, create_token, verify_token

router = APIRouter(tags=['User'])

@router.post('/add_user')
def add_user(input: User, db : Session = Depends(get_db)):
    hashedpwd = hash_password(input.password)
    new_user = data.User(**input.model_dump(exclude={'id', 'password'}), password = hashedpwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        'status': 'success',
        'data': new_user.email,
        'detail': 'new user created'
    }

@router.post('/login')
def login(input: Login, db: Session = Depends(get_db)):
    user = db.query(data.User).filter(data.User.email == input.email).first()
    if not user:
        return {
            'status': 'error',
            'detail': 'no such user'
        }
    else:
        if verify_password(input.password, user.password):
            token = create_token({'sub': user.email})
            return {
                'status': 'success',
                'access_token': token,
                'token_type': 'bearer',
                'detail': 'logined as ' + user.email
            }
        else:
            return {
                'status': 'error',
                'detail': 'password is incorrect'
            }
