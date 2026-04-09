from typing import Optional, List, Generator
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select, Column, String


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(String, unique=True, index=True))
    password: str = Field(nullable=False)  
    is_active: bool = Field(default=True)

class UserCreate(SQLModel):
    username: str
    password: str

class UserRead(SQLModel):
    id: int
    username: str
    is_active: bool

class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

app = FastAPI(title="API Educativa: Solo Usuario y Clave")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
   
        usuarios_iniciales = [
            User(username="admin", password="abc"),
            User(username="invitado", password="12345"),
            User(username="root", password="toor")
        ]
        for u in usuarios_iniciales:
            existing = session.exec(select(User).where(User.username == u.username)).first()
            if not existing:
                session.add(u)
        session.commit()



@app.post("/users", response_model=UserRead, status_code=201)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    user = User(**user_in.dict())
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return user

@app.get("/users", response_model=List[UserRead])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@app.get("/users/{id}", response_model=UserRead)
def get_user(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user: raise HTTPException(status_code=404)
    return user

@app.put("/users/{id}", response_model=UserRead)
def update_user(id: int, user_in: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user: 
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = user_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
        
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except:
        raise HTTPException(status_code=400, detail="Error al actualizar")
    return user

@app.delete("/users/{id}")
def delete_user(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user: 
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    session.delete(user)
    session.commit()
    return {"status": "success", "message": f"Usuario eliminado correctamente"}


@app.post("/login")
def login(payload: UserCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == payload.username)).first()
    
    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {"status": "success", "message": "Login exitoso"}