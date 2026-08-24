from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from bson import ObjectId

from database import users_collection
from models import UserCreate, UserLogin, UserResponse, Token
from auth_utils import get_password_hash, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def user_helper(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "role": user.get("role", "user"),
        "createdAt": user.get("createdAt", datetime.utcnow().isoformat())
    }

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticazione richiesta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token non valido o scaduto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload["sub"]
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=401, detail="Token non valido")

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="Utente non trovato")

    return user_helper(user)

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate):
    existing = await users_collection.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Un utente con questa email esiste già")

    now = datetime.utcnow().isoformat()
    hashed_pwd = get_password_hash(payload.password)
    
    user_dict = {
        "name": payload.name,
        "email": payload.email.lower(),
        "hashed_password": hashed_pwd,
        "role": "user",
        "createdAt": now
    }

    result = await users_collection.insert_one(user_dict)
    new_user = await users_collection.find_one({"_id": result.inserted_id})
    user_resp = user_helper(new_user)
    
    access_token = create_access_token(data={"sub": user_resp["_id"], "email": user_resp["email"]})
    return {"access_token": access_token, "token_type": "bearer", "user": user_resp}

@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    user = await users_collection.find_one({"email": payload.email.lower()})
    if not user:
        raise HTTPException(status_code=400, detail="Email o password errati")

    if not verify_password(payload.password, user.get("hashed_password", "")):
        raise HTTPException(status_code=400, detail="Email o password errati")

    user_resp = user_helper(user)
    access_token = create_access_token(data={"sub": user_resp["_id"], "email": user_resp["email"]})
    return {"access_token": access_token, "token_type": "bearer", "user": user_resp}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
