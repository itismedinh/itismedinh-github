from fastapi import FastAPI, Form
import uvicorn
from datetime import datetime
from pymongo.mongo_client import MongoClient

app = FastAPI()
myclient = MongoClient("mongodb+srv://1doahoacamtucau:123dinh789@chuyende-iot.ou6yz.mongodb.net/?retryWrites=true&w=majority&appName=ChuyenDe-IOT")
mydb = myclient['Buoi_9_IOT']
mycol = mydb['Muc_do_3']
current_id = 0

@app.post("/post_all_json")
async def send_data(data: dict):
    global current_id
    current_id += 1
    data_entry = {
        "id": current_id,
        "temperature": data['temperature'],
        "humidity": data['humidity'],
        "led1": data['led1'],
        "led2": data['led2'],
        "led3": data['led3'],
        "device_name": data['device_name'],
        "timestamp": str(datetime.now())
    }
    mycol.insert_one(data_entry)
    print(f'Save to MongoDB: {data_entry}')
    return {"OK"}

@app.post("/post_all_url")
async def send_data(
    temperature: float = Form(...),
    humidity: float = Form(...),
    led1: int = Form(...),
    led2: int = Form(...),
    led3: int = Form(...),
    device_name: str = Form(...)
):
    global current_id
    current_id += 1
    data_entry = {
        "id": current_id,
        "temperature": temperature,
        "humidity": humidity,
        "led1": led1,
        "led2": led2,
        "led3": led3,
        "device_name": device_name,
        "timestamp": str(datetime.now())
    }
    mycol.insert_one(data_entry)
    print(f'Save to MongoDB: {data_entry}')
    return {"OK"}

@app.post("/post_temp_json")
async def send_data(data: dict):
    global current_id
    current_id += 1
    data_entry = {
        "id": current_id,
        "temperature": data['temperature'],
        "device_name": data['device_name'],
        "timestamp": str(datetime.now())
    }
    mycol.insert_one(data_entry)
    print(f'Save to MongoDB: {data_entry}')
    return {"OK"}

@app.post("/post_humi_json")
async def send_data(data: dict):
    global current_id
    current_id += 1
    data_entry = {
        "id": current_id,
        "humidity": data['humidity'],
        "device_name": data['device_name'],
        "timestamp": str(datetime.now())
    }
    mycol.insert_one(data_entry)
    print(f'Save to MongoDB: {data_entry}')
    return {"OK"}

@app.post("/post_led1_json")
async def send_data(data: dict):
    global current_id
    current_id += 1
    data_entry = {
        "id": current_id,
        "led1": data['led1'],
        "device_name": data['device_name'],
        "timestamp": str(datetime.now())
    }
    mycol.insert_one(data_entry)
    print(f'Save to MongoDB: {data_entry}')
    return {"OK"}

@app.post("/post_led2_json")
async def send_data(data: dict):
    global current_id
    current_id += 1
    data_entry = {
        "id": current_id,
        "led2": data['led2'],
        "device_name": data['device_name'],
        "timestamp": str(datetime.now())
    }
    mycol.insert_one(data_entry)
    print(f'Save to MongoDB: {data_entry}')
    return {"OK"}

@app.post("/post_led3_json")
async def send_data(data: dict):
    global current_id
    current_id += 1
    data_entry = {
        "id": current_id,
        "led3": data['led3'],
        "device_name": data['device_name'],
        "timestamp": str(datetime.now())
    }
    mycol.insert_one(data_entry)
    print(f'Save to MongoDB: {data_entry}')
    return {"OK"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)