# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded

# app = FastAPI()


# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter

# @app.exception_handler(RateLimitExceeded)
# def rate_limit_handler(request:Request, exc: RateLimitExceeded):
#     return JSONResponse(
#         status_code=429,
#         content= {
#             "Detail":"Too Many Request"
#         }
#     )
    
# @app.get("/home")
# @limiter.limit("5/minute")
# def get_data(request: Request):
#     return {
#         "message": "Success"
#     }


# from fastapi import FastAPI
# import time
# import requests

# app = FastAPI()

# cache_data = []
# last_fetch = 0

# @app.get("/photos")
# def get_photos():
    
#     global cache_data, last_fetch
    
#     start = time.time()
    
#     if time.time() - last_fetch > 60:
#         print ("Fetching Fresh Data")
#         url = "https://jsonplaceholder.typicode.com/photos"
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         data = response.json()
        
#         cache_data = data
        
#         last_fetch = time.time()
#         end = time.time()
#         time_taken = round(end - start, 4)
        
#         return {
#             "Time Taken": time_taken,
#             "Total": len(data),
#             "Data":data
#         }
    
#     else:
#         print("Using Cache Data")
        
#         end = time.time()
#         time_taken = round(end - start, 4)
        
#         return{
#             "Time Taken": time_taken,
#             "Data": cache_data
#         }


# from fastapi import FastAPI,HTTPException
# import requests

# app = FastAPI()

# @app.get("/photos")
# def get_photos():
#     url = "https://jsonplaceholder.typicode.com/photos"
#     response = requests.get(url)
#     data = response.json()
#     return {
#         "Total":"len(data)",
#         "Data": data
#     }

# @app.get("/photos/{photo_id}")
# def get_photo(photo_id):
#     url = "https://jsonplaceholder.typicode.com/photos"
#     response = requests.get(url)
#     if response.status_code != 200:
#         raise HTTPException(status_code=404, detail="Page Not Found")
    
#     return response.json()


# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_home():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response .json() == {"Message":"Testing Page"}
    
# def test_add():
#     response = client.get("/add?a=6&b=5")
#     assert response.status_code == 200
#     assert response.json() == {"sum": 11}



# import os
# from config import settings
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# origins = settings.ORIGINS
# ORIGINS = os.getenv("ORIGINS")
# DB_URL = os.getenv("DATABASE_URL")
# SECRET_KEY = os.getenv("SECRET_KEY")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins= origins,
#     allow_methods=["*"],
#     allow_credentials=True,
#     allow_headers=["*"]
# )

# @app.get("/")
# def home():
#     return {
#         "message": "Cors Enable"
#     }


# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.staticfiles import StaticFiles
# import os 
# import shutil

# app = FastAPI()

# UPLOAD_DIR = "uploads"
# if not os.path.exists(UPLOAD_DIR):
#     os.makedirs(UPLOAD_DIR)
    
# app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# @app.post("/upload")
# def upload_file(file:UploadFile=File(...)):
#     filename = file.filename
#     file_path = os.path.join(UPLOAD_DIR, filename)
    
#     if not filename == file.filename:
#         raise HTTPException(
#             status_code=400,
#             detail="File not Selected"
#         )
        
#     with open(file_path,"wb") as buffer:
#         shutil.copyfileobj(file.file,buffer)
        
#     return {
#         "Message":"File Upload Successfully",
#         "filename": filename,
#         "file_url": f"http://127.0.0.1:8000/files/{filename}"
#     }
    

# @app.get("/files/{filename}")
# def get_file(filename:str):
#     file_path = os.path.join(UPLOAD_DIR, filename)
    
#     if not os.path.exists(file_path):
#         raise HTTPException(
#             status_code=404,
#             detail="File not Found"
#         )
        
#     return {
#         "file_url": f"http://127.0.0.1:8000/files/{filename}"
#     }
    

# @app.get("/")
# def home():
#     return{
#         "Message": "Here, You can upload the files"
#     }
    
    
    
    
# from fastapi import FastAPI,HTTPException,Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.context import CryptContext
# from datetime import datetime, timedelta, timezone
# from jose import jwt,JWTError


# app = FastAPI()

# SECRET_KEY = "mysecret"
# ALGORITHM = "HS256"

# pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")
# OAuth2_schema = OAuth2PasswordBearer(tokenUrl = "login")

# fake_user_db = {
#     "admin";{
#         "username":"admin",
#         "hashed_password": pwd_context.hash("12345")
#     }
# }

# def hash_password(password:str):
#     return pwd_context.hash(password)

# def verify_password(plain_password:str, hashed_password:str):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_token(data:dict):
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(minutes=30)
#     to_encode.update({
#         "exp": expire
#     })
    
#     token = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
#     return token

# @app.post("/login")
# def login(form_data:OAuth2PasswordRequestForm = Depends()):
#     user = fake_user_db.get(form_data.username)
#     if not user or not verify_password(form_data.password, user["hashed_password"]):
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid username or password"
#         )
        
#     access_token = create_token({"username":form_data.username})
    
#     return {
#         "access_token": access_token,
#         "token_type": "bearer"
#     }
    
# def verify_token(token:str = Depends(OAuth2_schema)):
#     try:
#         payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
#         username:str = payload.get("username")
#         if username is None:
#             raise HTTPException(
#                 status_code = 401,
#                 detail="Invalid Token"
#             )
            
#         return username
    
#     except JWTError:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid Token"
#         )
        
# @app.get("/protected")
# def protected_route(username:str=Depends(verify_token)):
#     return {
#         "message":"You have access this route",
#         "user": username
#     }



# from fastapi import FastAPI,HTTPException,Depends,Header
# from datetime import timedelta,timezone,datetime
# from jose import jwt

# app = FastAPI()

# SECRET_KEY = "mysecret"
# ALGORITHM = "HS256"

# def create_token(data:dict):
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(minutes=30)
#     to_encode.update({
#         "exp":expire
#     })
    
#     token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
#     return token

# @app.post("/login")
# def login(username:str, password:int):
#     if username != "rahul_21" or password != 7890:
#         raise HTTPException(
#             status_code=401,
#             detail= "Invalid Username or Password"
#         )
#     token = create_token({
#         "User":username
#     })
    
#     return {
#         "Access Token": token
#     }
    
# def verify_token(token:str = Header(None)):
#     try:
#         payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
#         return payload
#     except:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid or expired Token"
#         )
        
# @app.get("/dashboard")
# def dashboard(user = Depends(verify_token)):
#     return {
#         "message":"Dashboard Access",
#         "User": user
#     }




# from fastapi import FastAPI
# import asyncio
# import time

# app = FastAPI()

# def task():
#     time.sleep(3)
#     return "Done"

# async def task():
#     await asyncio.sleep(3)
#     return {
#         "Message": 'Async API'
#     }



# from fastapi import FastAPI,Depends, HTTPException
# from sqlalchemy import create_engine,Column,String,Integer
# from sqlalchemy.orm import sessionmaker,declarative_base,Session

# app = FastAPI()

# DATABASE_URL = "sqlite:///./user.db"

# engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

# sessionLocal = sessionmaker(bind=engine)

# Base = declarative_base()

# class Todo(Base):
#     __tablename__ ="UserDB"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     completed = Column(String)
    
# Base.metadata.create_all(bind=engine)

# def get_db():
    
#     db = sessionLocal()
    
#     try:
#         yield db 
        
#     finally:
#         db.close()
        
# @app.post("/todos")
# def create_todo(title:str, completed:str, db: Session = Depends(get_db)):
#     todo = Todo(title = title, completed = completed)
#     db.add(todo)
#     db.commit()
#     db.refresh(todo)
#     return{
#         "message":"Todo Created",
#         "Data": todo
#     }
    
# @app.get("/todos")
# def get_todo(db:Session = Depends(get_db)):
#     todos = db.query(Todo).all()
#     return {
#         "Total":len(todos),
#         "Data": todos
#     }
    
# @app.get("/todos/{todo_id}")
# def get_todo(todo_id: int, db:Session = Depends(get_db)):
#     todo =  db.query(Todo).filter(Todo.id == todo_id).first()
#     if not todo:
#         raise HTTPException(status_code=404, detail="Todo not Found")
#     return todo

# @app.put("/todos/{todo_id}")
# def update_todo(todo_id: int, title:str, db:Session = Depends(get_db)):
#     todo = db.query(Todo).filter(Todo.id==todo_id).first()
#     if not todo:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     todo.title = title
#     db.commit()
#     db.refresh(todo)
#     return{
#         "Message": "Todo Updated",
#         "Data": todo
#     }
    
# @app.delete("/todos/{todo_id}")
# def delete_todo(todo_id:int, db: Session = Depends(get_db)):
#     todo = db.query(Todo).filter(Todo.id == todo_id).first()
#     if not todo:
#         raise HTTPException(status_code=404, detail="Todo not Found")
    
#     db.delete(todo)
#     db.commit()
#     return {
#         "message":"Todo Deleted"
#     }



# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import sessionmaker,declarative_base,Session
# from fastapi import FastAPI,Depends

# app = FastAPI()

# DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

# sessonLocal = sessionmaker(bind=engine)

# Base = declarative_base()

# class Todo(Base):
#     __tablename__ = "Todos"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     completed = Column(String)
    
# Base.metadata.create_all(bind=engine)

# def get_db():
#     db = sessionLocal()
    
#     try:
#         yield db
        
#     finally:
#         db.close()
        
# @app.get("/")
# def home(db: Session = Depends(get_db)):
#     return{
#         "message":"DB Connected"
#     }




from fastapi import FastAPI,Request
import time

app = FastAPI()

@app.middleware("http")
async def my_middleware(request:Request, call_next):
    print("Request Received")
    
    response = await call