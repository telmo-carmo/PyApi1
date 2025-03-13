'''
A simple FASTAPI aplication.

https://pyjwt.readthedocs.io/en/latest/usage.html#registered-claim-names

---

pip install -U fastapi uvicorn PyJWT Jinja2 python-multipart sqlalchemy psycopg2

--

fastapi dev --port 8080 main.py

uvicorn main:app --host 0.0.0.0 --port 80

uvicorn main:app --reload 

'''

import datetime, os
import json

import random
import platform
import sys

from fastapi import Depends, FastAPI, Form, HTTPException, Response, UploadFile, status, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Optional, Union

from sqlalchemy import create_engine, Column, Float, String, Boolean, Integer
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import jwt

from models import ItemRequest, ItemResponse, LoginReq, LoginResp
from applogger import logger

# Define database connection details (modify as needed)
SQLALCHEMY_DATABASE_URL = "sqlite:///./mydb1.db"
JWT_SECRET_KEY = "0d73b71d9d865136056f7365160edcef0db2440e94f56ba4e7f613e2d5ef91d7"  # 256 bit sk
JWT_ALGORITHM = "HS256"
UPLOAD_PATH = "C:/Uploads/Testes/" if platform.system() == "Windows"else "/tmp/Testes/"

# Create engine and session maker
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


App_ver = 1.05

logger.info('App version %.2f with db: %s', App_ver,SQLALCHEMY_DATABASE_URL)
##----------

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Item(Base):
    __tablename__ = "myitems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)
    is_offer =  Column(Boolean)

class Bonus(Base):
    __tablename__ = "bonus"
    ename = Column(String, primary_key=True, index=True)
    job =   Column(String, )
    sal =   Column(Integer)
    comm =  Column(Integer)


# Create database tables (run this once)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get a database session
def get_session_db(db: Session = Depends(get_db)):
    return db


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
  """
  This function checks the provided credentials against 
  predefined username and password (replace with your own)
  """
  #username = "your_username"
  password = "123"
  #if credentials.username != username or credentials.password != password:
  if credentials.password != password:
      raise HTTPException(
          status_code=401,
          detail="Incorrect username or password",
          headers={"WWW-Authenticate": "Basic"},
      )
  return credentials.username

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token,JWT_SECRET_KEY , algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
    
def get_current_jwt(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

@app.get("/")
async def read_root():
    return {"Hello": "FastAPI", "Version":  App_ver, "Now": datetime.datetime.now() }

@app.get("/home/{id}", response_class=HTMLResponse)
async def read_home(request: Request,id : str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id, 
            "items": [f"app ver {App_ver}", sys.version, datetime.datetime.now().isoformat() ]}
    )

@app.post("/prot")
async def post_protected_data(data: Optional[dict] = None, username: str = Depends(get_current_username)):
  """
  This endpoint handles the POST request. 
  - data: Optional data sent in the request body (can be modified)
  - username: Username retrieved from the dependency
  """
  # Perform actions with the data and username
  logger.warning("Current user = %s", username)
  return {"message": f"Hello, {username}! You sent: {data}"}

@app.get("/random-int")
async def get_random_int(min: int = 1, max: int = 100, current_jwt: dict = Depends(get_current_jwt)):
    random_int = random.randint(min, max)
    logger.warning("get random_int=%d (for %s)",random_int,current_jwt['sub'])
    return {"random_int": random_int}

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, session: Session = Depends(get_session_db)):
    logger.warning("get item id=%d",item_id)
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        logger.error("no item id=%d",item_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item {item_id} not found")
    return item


@app.put("/items/{item_id}",response_model=ItemResponse)
def update_item(item_id: int, item: ItemRequest, session: Session = Depends(get_session_db)):
    existing_it = session.query(Item).filter(Item.id == item_id).first()
    if not existing_it:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {item_id} not found")
    existing_it.name = item.name
    existing_it.price = item.price
    existing_it.is_offer = item.is_offer
    session.commit()
    return existing_it

@app.post("/items",status_code=status.HTTP_201_CREATED,response_model=ItemResponse)
def create_item(it: ItemRequest, session: Session = Depends(get_session_db)):
    # Create a new  object in db
    item = Item(name=it.name,price=it.price,is_offer=it.is_offer)
    # Add the user to the session
    session.add(item)
    # Save the changes to the database
    session.commit()
    session.refresh(item)  # Refresh to get generated ID
    return item

@app.get("/items", response_model=list[ItemResponse])
def get_items(session: Session = Depends(get_session_db)):
    items = session.query(Item).all()
    logger.info(f"Items # {len(items)}")
    return items

# Delete a item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session_db)):
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    session.delete(item)
    session.commit()
    return {"message": f"item {item_id} deleted successfully"}

@app.post("/auth/login",response_model=LoginResp)
async def login(reqData: LoginReq, db_session: Session = Depends(get_session_db)):
    logger.info("login(%s,%s)",reqData.uid,reqData.pwd)
    if reqData.pwd != "123":
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login data")
        data = {"error": "bad credentials",  "token": None}
        return Response(content=json.dumps(data), media_type="application/json", status_code=401)
    
    expires_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60)
    payload = {"sub": reqData.uid, "id": 11, "exp": expires_at}
    tok = jwt.encode(payload,JWT_SECRET_KEY,algorithm=JWT_ALGORITHM)
    # expires=expires_at.isoformat()
    return LoginResp(token='Bearer ' +tok,error=None,username=reqData.uid)


@app.post("/auth/chktoken")
async def check_token(req: LoginResp):
    try:
        data = jwt.decode(req.token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as ex1:
        logger.error(ex1)     # Signature has expired
        return  {"status": "jwt expired!"}
    logger.info(data)
    expires = data['exp']
    dt1 = datetime.datetime.fromtimestamp(expires,datetime.timezone.utc)
    logger.warning("expires: %d -- utc time: %s",expires,dt1.isoformat())
    return data

@app.get("/auth/rnd")
async def auth_rnd(current_jwt: dict = Depends(get_current_jwt)):
    rnd = random.random() 
    logger.info("Current JWT " + str(current_jwt))
    return rnd
    #return {"message": "This is a protected route", "rn": rnd, "user": current_jwt['sub'] }


@app.get("/upload")
async def upload_list(request: Request):
    lst1 = os.listdir(UPLOAD_PATH)
    return templates.TemplateResponse(name="upload1.html", request=request, 
                                      context={ "docid": "id-1234", "mydocs": lst1})

@app.post("/upload")
async def create_upload_file(pid : str = Form(...), file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        fname =  UPLOAD_PATH + file.filename
        fcontents = await file.read()
        with open(fname, "wb") as f:
            f.write(fcontents)
        logger.info("pid=%s: Uploaded file: %s",pid, fname)
        return {"proc-id": pid, "filename": file.filename, "size": file.size}


@app.post("/api/echo")
async def api_echo(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    logger.info("Api Echo data:%s",data)
    return {"Echo": "FastAPI", "req": data }

@app.get("/api/bonus")
async def get_bonus(session: Session = Depends(get_session_db)):
    items = session.query(Bonus).all()
    logger.info(f"Bonus # {len(items)}")
    return items

@app.get("/api/bonus/{item_id}")
async def get_one_bonus(item_id: str, session: Session = Depends(get_session_db)):
    logger.warning("get bonus id=%s",item_id)
    item = session.query(Bonus).filter(Bonus.ename == item_id).first()
    if not item:
        logger.error("no item id=%d",item_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"bonus ename={item_id} not found")
    return item




if __name__ == "__main__":
    import uvicorn
    #uvicorn.run("main:app", port=8000, log_level="info")
    
    uvicorn.run(app,port=8080)
    ## run with https self signed cert:
    ##uvicorn.run(app, host="localhost", port=8083, ssl_certfile="server.crt", ssl_keyfile="server.key") # run in https mode
