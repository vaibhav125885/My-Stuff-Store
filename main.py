from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db,StuffDB,UserDB
from fastapi.middleware.cors import CORSMiddleware
from auth import (hash_password,verify_password,get_current_user,admin_required,create_token)
 
 
app = FastAPI()

origins = [
"http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"]
)

class Stuff(BaseModel):
    id: int
    name: str
    price: int
    
class UserCreate(BaseModel):
    username: str
    password: str

class LoginData(BaseModel):
    username: str
    password: str
    
    
# Register API

@app.post("/register")
def register(user: UserCreate,db: Session = Depends(get_db)):

    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)

    new_user = UserDB(
        username=user.username,
        password=hashed_password,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "username": new_user.username,
        "role": new_user.role
    }
    
    
# Login API


@app.post("/login")
def login(user: LoginData,db: Session = Depends(get_db)):

    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password( user.password, db_user.password):
        
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_token(
        {
            "sub": db_user.username,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
    
# User Access

@app.get("/")
def home(current_user: UserDB = Depends(get_current_user)):
    return {
        "message":"Welcome To Healthy Stuff Store"
    }
    

@app.get("/stuff")
def get_stuffs(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    
    stuff = db.query(StuffDB).all()
    return {
        "Toatal Stuff": len(stuff),
        "Stuff": stuff 
    }

@app.get("/stuff/{stuff_id}")
def get_stuff(stuff_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    stuff = db.query(StuffDB).filter(StuffDB.id==stuff_id).first()
    if not stuff:
        raise HTTPException(status_code=404, detail="Gaaand Maraaaa")
    return {
        "Product": stuff
    }


# Admin Access

@app.post("/stuff")
def add_stuff(stuff:Stuff, db: Session = Depends(get_db), current_user: UserDB = Depends(admin_required)):
     
    new_stuff = StuffDB(
         id = stuff.id,
         name = stuff.name,
         price = stuff.price
        )
    
    db.add(new_stuff)
    db.commit()
    db.refresh(new_stuff)
    
    return {
        "message":"Stuff Created",
        "Product": new_stuff
    }


@app.put("/stuff/{stuff_id}")
def update_stuff(stuff_id: int, updated_stuff:Stuff, db: Session = Depends(get_db), current_user: UserDB = Depends(admin_required)):
    
    stuff = db.query(StuffDB).filter(StuffDB.id==stuff_id).first()
    
    if not stuff:
        raise HTTPException(status_code=404, detail="Gaaand Maraaaa")
    
    stuff.id = updated_stuff.id
    stuff.name = updated_stuff.name
    stuff.price = updated_stuff.price
    
    
    db.commit()
    db.refresh(stuff)
        
    return {
            "message":"Stuff Created",
            "Product": stuff
        }
    
@app.delete("/stuff/{stuff_id}")
def delete_stuff(stuff_id: int, db: Session = Depends(get_db),current_user: UserDB = Depends(admin_required)):
    
    stuff = db.query(StuffDB).filter(StuffDB.id==stuff_id).first()
    
    if not stuff:
        raise HTTPException(status_code=404, detail="Gaaand Maraaaa")
    
    db.delete(stuff)
    db.commit()
    return {
        "Message": "Stuff Delete"
    }







# products = {}
# @app.get("/")
# def home():
#     return {
#         "message":"Welcome To The Server"
#     }
    
# @app.post("/product")
# def create_product(product:Product):
#     products[product.id] = product
#     return product

# @app.get("/product")
# def get_products():
#     return {
#         "Product": products
#     }

# @app.get("/product/{product_id}")
# def get_product(product_id: int):
#     for product in products:
#         if product == product_id:
#             return products[product_id]
#     raise HTTPException(status_code=404, detail="Product Not 
# def update_product(product_id: int, updated_product:Product):
#     for product in products:
#         if product == product_id:
#             products[product_id] = updated_product
#             return {
#                 "message":"Product Updated"
#     raise HTTPException(status_code=404, detail="Product Not Found")