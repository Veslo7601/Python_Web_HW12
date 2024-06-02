from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from My_project.database.database import get_database
from My_project.database.models import User
from My_project.repository.auth import create_access_token, create_refresh_token, get_email_from_refresh_token, get_current_user, Hash
from My_project.schemas import UserModel, UserResponse



router = APIRouter(prefix="/autentification")
hash = Hash()
security = HTTPBearer()

@router.post("/signup", response_model=UserResponse)
async def singup(body: UserModel, db: Session = Depends(get_database)):

    user_exist = db.query(User).filter(User.email == body.username).first()
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    new_user = User(email=body.username, password=hash.get_password_hash(body.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"new_user": new_user.email}

router.post("/login")
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database)):
    exist_user = db.query(User).filter(User.email == body.username).first()
    if exist_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not hash.verify_password(body.password, exist_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    access_token = await create_access_token(data={"sub":exist_user.email})
    refresh_token = await create_refresh_token(data={"sub": exist_user.email})
    exist_user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

router.get('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_database)):
    token = credentials.credentials
    email = await get_email_from_refresh_token(token)
    user = db.query(User).filter(User.email == email).first()
    if user.refresh_token != token:
        user.refresh_token = None
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await create_access_token(data={"sub": email})
    refresh_token = await create_refresh_token(data={"sub": email})
    user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

router.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": 'secret router', "owner": current_user.email}
