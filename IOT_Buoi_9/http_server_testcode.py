# Import các thư viện cần thiết 
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from datetime import datetime
from pymongo.mongo_client import MongoClient
import json
import urllib.parse

# Khởi tạo ứng dụng FastAPI 
app = FastAPI()

# Thực hiện kết nối tới MongoDB
myclient = MongoClient("mongodb+srv://1doahoacamtucau:123dinh789@iotbuoi8http.ou6yz.mongodb.net/?retryWrites=true&w=majority&appName=IotBuoi8Http")
mydb = myclient['iot']
mycol = mydb['Muc_do_3']
current_id = 0

# Lớp Dataclass tự định nghĩa gồm các dữ liệu id, nhiệt độ, độ ẩm, 3 LED, tên thiết bị gửi dữ liệu và thời gian gửi 
class DataClass(BaseModel):
    id: int
    temperature: float
    humidity: float
    led1: int
    led2: int
    led3: int
    device_name: str
    timestamp: str

# Hàm gửi dữ liệu lên database
@app.post("/post")
async def send_data(data: DataClass):
    global current_id
    current_id += 1
    data_entry = {
        "id": current_id,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "led1": data.led1,
        "led2": data.led2,
        "led3": data.led3,
        "device_name": data.device_name,
        "timestamp": str(datetime.now())
    }
    # mycol.insert_one(data_entry)
    print(f'Save to MongoDB: {data_entry}')
    return {"OK"}

# @app.post("/post")
# async def get_data(item: Item):
#     my_dict = {
#         "data1": item.data1,
#         "data2": item.data2
#     }
#     print(my_dict)
#     return {"OK"}

# @app.get("/get")
# async def get_data():
#     all_data = mycol.find().sort("timestamp", -1)
#     return {"all_data": list(all_data)}

# Thực hiện chạy ứng dụng qua địa chỉ 0.0.0.0 (nhận mọi kết nối) và cổng 8000    
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)