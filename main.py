from fastapi import FastAPI, UploadFile, Form
from sqlalchemy.orm import sessionmaker
from fastapi.responses import FileResponse
from db import Item, engine
import random, string, shutil

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'hello world'}

@app.post('/item')
def item_post(latitude: float = Form(float), longitude: float = Form(float), image: UploadFile = Form(UploadFile), audio: UploadFile = Form(UploadFile)):
    img_ex = image.filename.split('.')[-1]
    img_path = f'./images/{randomname(30)}.{img_ex}'
    with open(img_path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
    aud_ex = audio.filename.split('.')[-1]
    aud_path = f'./audios/{randomname(30)}.{aud_ex}'
    with open(aud_path, 'w+b') as buffer:
        shutil.copyfileobj(audio.file, buffer)
    ses = SessionLocal()
    item = Item(latitude = latitude, longitude = longitude, imagepath=img_path, audiopath=aud_path)
    ses.add(item)
    ses.commit()
    return { 'status': 'ok', 'id': item.id}

@app.get('/item')
def item_get(id: int):
    ses = SessionLocal()
    item = ses.query(Item).filter(Item.id==id).first()
    if item is None:
        return { 'status': 'ng' }
    return {
        'status': 'ok',
        'id': item.id,
        'latitude': item.latitude,
        'longitude': item.longitude,
        'get_image_url': '/item/image',
        'get_audio_url': '/item/audio'
    }
    
@app.get('/items')
def items_get():
    ses = SessionLocal()
    item = ses.query(Item).all()
    res = []
    for i in item:
        res.append({
            'id': i.id,
            'latitude': i.latitude,
            'longitude': i.longitude
        })
    return {
        'status': 'ok',
        'items': res
    }
        

@app.get('/item/image')
def item_image_get(id: int):
    ses = SessionLocal()
    item = ses.query(Item).filter(Item.id==id).first()
    if item is None or item.imagepath is None:
        return { 'status': 'ng' }
    file_path = item.imagepath
    file_name = item.imagepath.split('/')[-1]
    return FileResponse(
        path=file_path,
        filename=file_name
    )
    
@app.get('/item/audio')
def item_audio_get(id: int):
    ses = SessionLocal()
    item = ses.query(Item).filter(Item.id==id).first()
    if item is None or item.imagepath is None:
        return { 'status': 'ng' }
    file_path = item.audiopath
    file_name = item.audiopath.split('/')[-1]
    return FileResponse(
        path=file_path,
        filename=file_name
    )
    