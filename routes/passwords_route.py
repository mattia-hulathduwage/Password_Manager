from fastapi import APIRouter, Depends, HTTPException
from schemas.passwords_schema import Passwords
import database.database_model as data
from dependency import get_db, encrypt_pwd, decrypt_pwd
from sqlalchemy.orm import session
from auth import verify_token
from datetime import date

router = APIRouter(tags=['passwords'])

@router.post('/add_password')
def add_password(input: Passwords, db: session = Depends(get_db), token: str = Depends(verify_token)):
    updated_date = date.today()
    pwd_encrypted = encrypt_pwd(input.password)
    new_password = data.Passwords(**input.model_dump(exclude={'id', 'user', 'last_updated', 'password'}), user = token.id, last_updated = updated_date, password = pwd_encrypted)
    db.add(new_password)
    db.commit()
    db.refresh(new_password)
    return {
        'status': 'success',
        'detail': 'new password added for ' + new_password.title
    }

@router.get('/get_passwords')
def get_passwords(db: session = Depends(get_db), token: str = Depends(verify_token)):
    Passwords = db.query(data.Passwords).filter(data.Passwords.user == token.id).all()
    if not Passwords:
        return {
            'status': 'error',
            'detail': 'no passwords found'
        }
    else:
        return {
            'status': 'success',
            'data': Passwords
        }
    
@router.delete('/delete_password/{id}')
def delete_password(id: int, db: session = Depends(get_db), token: str = Depends(verify_token)):
    password = db.query(data.Passwords).filter(data.Passwords.id == id, data.Passwords.user == token.id).first()
    if not password:
        return {
            'status': 'error',
            'detail': 'no such password found'
        }
    else:
        db.delete(password)
        db.commit()
        return {
            'status': 'success',
            'detail': 'password deleted successfully'
        }
    
@router.get('/get_password/{id}')
def get_password(id: int, db: session = Depends(get_db), token: str = Depends(verify_token)):
    password_user = db.query(data.Passwords).filter(data.Passwords.id == id, data.Passwords.user == token.id).first()
    if not password_user:
        return {
            'status': 'error',
            'detail': 'no password found'
        }
    else:
        return {
            'status': 'success',
            'data': {
                'id': password_user.id,
                'title': password_user.title,
                'password': decrypt_pwd(password_user.password),
                'last_updated': password_user.last_updated
            }
        }
    
@router.put('/update_password/{id}')
def update_password(id: str, input: Passwords, db: session = Depends(get_db), token: str = Depends(verify_token)):
    select_password = db.query(data.Passwords).filter(data.Passwords.id == id, data.Passwords.user == token.id).first()
    if not select_password:
        return {
            'status': 'error',
            'detail': 'password not found'
        }
    else:
        select_password.title = input.title
        select_password.password = encrypt_pwd(input.password)
        select_password.last_updated = date.today()

        db.commit()
        db.refresh(select_password)

        return {
            'status': 'success',
            'data': {
                'id': select_password.id,
                'title': select_password.title,
                'password': decrypt_pwd(select_password.password),
                'last_updated': select_password.last_updated
            }
        }
