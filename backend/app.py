
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import databases, sqlalchemy, os
from passlib.context import CryptContext
from uuid import uuid4
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./skillarena.db')
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

users = sqlalchemy.Table(
    'users', metadata,
    sqlalchemy.Column('id', sqlalchemy.String, primary_key=True),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column('username', sqlalchemy.String),
    sqlalchemy.Column('password_hash', sqlalchemy.String),
    sqlalchemy.Column('is_admin', sqlalchemy.Boolean, default=False),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime, default=datetime.utcnow)
)

lounges = sqlalchemy.Table(
    'lounges', metadata,
    sqlalchemy.Column('id', sqlalchemy.String, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('currency', sqlalchemy.String),
    sqlalchemy.Column('min_entry', sqlalchemy.Integer, default=0),
    sqlalchemy.Column('jackpot', sqlalchemy.Integer, default=0)
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {})
metadata.create_all(engine)

app = FastAPI(title='SkillArena API')

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

@app.on_event('startup')
async def startup():
    await database.connect()
    # seed admin
    q = users.select().where(users.c.email == 'admin@skillarena.com')
    admin = await database.fetch_one(q)
    if not admin:
        pwd = pwd_context.hash('SkillArena@2025')
        await database.execute(users.insert().values(id=str(uuid4()), email='admin@skillarena.com', username='admin', password_hash=pwd, is_admin=True, created_at=datetime.utcnow()))
    # seed lounges
    r = await database.fetch_all(lounges.select())
    if not r:
        await database.execute(lounges.insert().values(id=str(uuid4()), name='Free Lounge', currency='FREE', min_entry=0, jackpot=0))
        await database.execute(lounges.insert().values(id=str(uuid4()), name='Standard Lounge', currency='NGN', min_entry=50, jackpot=0))
        await database.execute(lounges.insert().values(id=str(uuid4()), name='Premium Lounge', currency='NGN', min_entry=200, jackpot=0))

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

@app.post('/auth/register')
async def register(u: UserCreate):
    q = users.select().where(users.c.email == u.email)
    found = await database.fetch_one(q)
    if found:
        raise HTTPException(status_code=400, detail='Email already registered')
    pwd = pwd_context.hash(u.password)
    await database.execute(users.insert().values(id=str(uuid4()), email=u.email, username=u.username, password_hash=pwd, is_admin=False, created_at=datetime.utcnow()))
    return {'ok': True, 'email': u.email}

@app.post('/auth/login')
async def login(u: UserCreate):
    q = users.select().where(users.c.email == u.email)
    found = await database.fetch_one(q)
    if not found or not pwd_context.verify(u.password, found['password_hash']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return {'ok': True, 'email': found['email'], 'username': found['username']}

@app.get('/lounges')
async def get_lounges():
    return await database.fetch_all(lounges.select())

@app.get('/support')
async def support():
    return {'whatsapp':'+2347011695248', 'call':'+2347053070533', 'email':'kennygalubeze@gmail.com' }

@app.get('/health')
async def health():
    return {'ok': True, 'app': 'SkillArena', 'ts': datetime.utcnow().isoformat()}
