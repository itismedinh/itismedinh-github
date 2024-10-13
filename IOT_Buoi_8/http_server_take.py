from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse
import uvicorn
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi.security.api_key import APIKeyHeader
from pymongo.mongo_client import MongoClient
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = FastAPI()
api_write_header = APIKeyHeader(name="api_write")
API_WRITE = "nhom11-write"
api_read_header = APIKeyHeader(name="api_read")
API_READ = "nhom11-read"
myclient = MongoClient("mongodb+srv://1doahoacamtucau:123dinh789@iotbuoi8http.ou6yz.mongodb.net/?retryWrites=true&w=majority&appName=IotBuoi8Http")
mydb = myclient['iot']
mycol = mydb['Muc_do_3']

# class Item(BaseModel):
#     data1: float
#     data2: float

class SensorData(BaseModel):
    temperature: float
    humidity: float
    led1: int
    led2: int
    led3: int
    device_name: str

class SensorDataResponse(SensorData):
    id: int
    timestamp: datetime

def verify_api_write(api_key: str = Depends(api_write_header)):
    if api_key != API_WRITE:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return None

def verify_api_read(api_key: str = Depends(api_read_header)):
    if api_key != API_READ:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return None

@app.post("/api", dependencies=[Depends(api_write_header)])
async def send_data(data: SensorData):
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
    mycol.insert_one(data_entry)
    return {"message": "Data received", "temperature": data_entry["temperature"]}

@app.get("/api/get_data", response_model=List[SensorDataResponse], dependencies=[Depends(verify_api_read)])
async def get_data(
    n: Optional[int] = Query(None, description="Số lượng dữ liệu gần nhất"),
    start_time: Optional[str] = Query(None, description="Thời gian bắt đầu (ISO format)"),
    end_time: Optional[str] = Query(None, description="Thời gian kết thúc (ISO format)")
):

    print(f"Received n: {n}, start: {start_time}, end: {end_time}")

    # Nếu cung cấp n, truy xuất N dữ liệu gần nhất
    if n is not None and start_time is None and end_time is None:
        cursor = mycol.find().sort("_id", -1).limit(n)  # Lấy n dữ liệu mới nhất
        return list(cursor)
    
    # Nếu cung cấp start_time và end_time, truy xuất theo khoảng thời gian
    if n is None and start_time and end_time:
        cursor = mycol.find({
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        }).sort("timestamp", 1)
        return list(cursor)
    
    if n is not None and start_time and end_time:
        cursor = mycol.find({
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        }).sort("timestamp", 1).limit(n)
        return list(cursor)
    
    # Nếu không có tham số nào, trả về 5 dữ liệu
    cursor = mycol.find().sort("_id", -1).limit(5)
    return list(cursor)

def fetch_data(n=None, start_time=None, end_time=None):
    # Nếu cung cấp n, truy xuất N dữ liệu gần nhất
    if n is not None and start_time is None and end_time is None:
        cursor = mycol.find().sort("_id", -1).limit(n)
        return list(cursor)

    # Nếu cung cấp start_time và end_time, truy xuất theo khoảng thời gian
    if n is None and start_time and end_time:
        cursor = mycol.find({
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        }).sort("timestamp", 1)
        return list(cursor)

    # Trường hợp có n và khoảng thời gian
    if n is not None and start_time and end_time:
        cursor = mycol.find({
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        }).sort("timestamp", 1).limit(n)
        return list(cursor)

    # Nếu không có tham số nào, trả về 5 dữ liệu gần nhất
    cursor = mycol.find().sort("_id", -1).limit(5)
    return list(cursor)

def plot_line_chart(temp, humi, id_graph, led1_state, led2_state, led3_state):
    
    
    # Chuyển đổi ObjectId thành chuỗi
    # id_graph_str = [str(id) for id in id_graph]
    x_values = list(range(0,5))
    
    # Vẽ các đường biểu đồ
    plt.subplot(3,2,1)
    plt.plot(x_values, temp, label='Temperature')
    plt.title('Biểu Đồ Nhiệt Độ')
    plt.subplot(3,2,2)
    plt.plot(x_values, humi, label='Humidity')
    plt.title('Biểu Đồ Độ Ẩm')
    plt.subplot(3,2,3)
    plt.plot(x_values, led1_state, label='LED1 State')
    plt.title('Biểu Đồ LED 1')
    plt.subplot(3,2,4)
    plt.plot(x_values, led2_state, label='LED2 State')
    plt.title('Biểu Đồ LED 2')
    plt.subplot(3,2,5)
    plt.plot(x_values, led3_state, label='LED3 State')
    plt.title('Biểu Đồ LED 3')
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    print(temp, humi, led1_state, led2_state, led3_state)
    
    # Lưu biểu đồ dưới dạng ảnh base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return img_base64

@app.get("/graph", response_class = HTMLResponse)
def graph():
    data = fetch_data(n=5)
    temp = [d['temperature'] for d in data]
    humi = [d['humidity'] for d in data]
    id_graph = [d['_id'] for d in data]
    led1_state = [d['led1'] for d in data]
    led2_state = [d['led2'] for d in data]
    led3_state = [d['led3'] for d in data]
    img = plot_line_chart(temp, humi, id_graph, led1_state, led2_state, led3_state)
    html = f"""<!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Biểu Đồ Dữ Liệu</title>
            <meta http-equiv="refresh" content="5">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    text-align: center;
                    padding: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    border: 2px solid #2c3e50;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
            </style>
        </head>
        <body>
            <h1>Hiển Thị Dữ Liệu</h1>
            <img src="data:image/png;base64,{img}" alt="Biểu Đồ Dữ Liệu" />
        </body>
        </html>"""
    return html

current_id = 0

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)