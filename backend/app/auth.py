import os
from datetime import datetime,timedelta
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto'); oauth=OAuth2PasswordBearer(tokenUrl='/api/auth/login')
SECRET=os.getenv('JWT_SECRET','dev-only-change-me'); ALG='HS256'
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def token_for(u): return jwt.encode({'sub':str(u.id),'exp':datetime.utcnow()+timedelta(days=7)},SECRET,algorithm=ALG)
def current_user(token:str=Depends(oauth),db:Session=Depends(get_db)):
 try: uid=int(jwt.decode(token,SECRET,algorithms=[ALG])['sub'])
 except (JWTError,ValueError): raise HTTPException(401,'Invalid or expired token')
 u=db.get(User,uid)
 if not u: raise HTTPException(401,'User not found')
 return u
