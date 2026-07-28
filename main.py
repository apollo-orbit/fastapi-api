from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="API Chida",
    description="API simple con FastAPI",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DUMMY_USERS = [
    {"id": 1, "name": "Alejandro Ram\u00edrez", "email": "alex@99labs.co", "role": "admin"},
    {"id": 2, "name": "Mar\u00eda Garc\u00eda", "email": "maria@example.com", "role": "user"},
    {"id": 3, "name": "Carlos L\u00f3pez", "email": "carlos@example.com", "role": "user"},
    {"id": 4, "name": "Ana Torres", "email": "ana@example.com", "role": "editor"},
    {"id": 5, "name": "Luis Hern\u00e1ndez", "email": "luis@example.com", "role": "user"},
]

class UserCreate(BaseModel):
    name: str
    email: str
    role: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

@app.get("/")
def root():
    return {"message": "\u00a1Que onda, mundo!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/users")
def get_users():
    return {"users": DUMMY_USERS, "count": len(DUMMY_USERS)}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = next((u for u in DUMMY_USERS if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}

def _email_exists(email: str, exclude_id: Optional[int] = None) -> bool:
    return any(
        u["email"].lower() == email.lower() and u["id"] != exclude_id
        for u in DUMMY_USERS
    )

@app.post("/users")
def create_user(user: UserCreate):
    if _email_exists(user.email):
        raise HTTPException(status_code=409, detail=f"Email '{user.email}' already exists")
    new_id = max(u["id"] for u in DUMMY_USERS) + 1
    new_user = {"id": new_id, "name": user.name, "email": user.email, "role": user.role}
    DUMMY_USERS.append(new_user)
    return {"user": new_user, "message": "User created"}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    existing = next((u for u in DUMMY_USERS if u["id"] == user_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    if user.email is not None and _email_exists(user.email, exclude_id=user_id):
        raise HTTPException(status_code=409, detail=f"Email '{user.email}' already exists")
    if user.name is not None:
        existing["name"] = user.name
    if user.email is not None:
        existing["email"] = user.email
    if user.role is not None:
        existing["role"] = user.role
    return {"user": existing, "message": "User updated"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global DUMMY_USERS
    user = next((u for u in DUMMY_USERS if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    DUMMY_USERS = [u for u in DUMMY_USERS if u["id"] != user_id]
    return {"message": "User deleted", "user": user}
