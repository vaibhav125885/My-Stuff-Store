from db import SessionLocal, UserDB

db = SessionLocal()

user = db.query(UserDB).filter(UserDB.username == "admin").first()

if user:
    user.role = "admin"
    db.commit()
    print("Admin successfully created!")
else:
    print("Admin user not found!")

db.close()