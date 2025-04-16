from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import uuid
import redis  #  Redis added

app = FastAPI()

# In-memory storage
houses = {}
users = {}

# Redis client setup
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Models
class Metadata(BaseModel):
    description: Optional[str] = None
    location: Optional[str] = None

class Device(BaseModel):
    id: Optional[str] = None
    name: str
    type: str
    data: dict

class Room(BaseModel):
    id: Optional[str] = None
    name: str
    metadata: Optional[Metadata] = None
    devices: List[Device] = []

class Floor(BaseModel):
    id: Optional[str] = None
    name: str
    metadata: Optional[Metadata] = None
    rooms: List[Room] = []

class House(BaseModel):
    id: Optional[str] = None
    name: str
    metadata: Optional[Metadata] = None
    floors: List[Floor] = []

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str

# --- USER ENDPOINTS ---

@app.post("/users/")
def create_user(user: User):
    user.id = str(uuid.uuid4())
    users[user.id] = user
    return user

@app.get("/users/{user_id}")
def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.put("/users/{user_id}")
def update_user(user_id: str, name: Optional[str] = None, email: Optional[str] = None):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if name:
        users[user_id].name = name
    if email:
        users[user_id].email = email
    return users[user_id]

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"message": f"User {user_id} deleted successfully"}

# --- HOUSE ENDPOINTS ---

@app.post("/houses/")
def create_house(house: House):
    house.id = str(uuid.uuid4())
    houses[house.id] = house
    return house

@app.get("/houses/{house_id}")
def get_house(house_id: str):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    return houses[house_id]

@app.put("/houses/{house_id}")
def update_house(house_id: str, name: Optional[str] = None):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    if name:
        houses[house_id].name = name
    return houses[house_id]

@app.delete("/houses/{house_id}")
def delete_house(house_id: str):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    del houses[house_id]
    return {"message": f"House {house_id} deleted successfully"}

# --- FLOOR ENDPOINTS ---

@app.post("/houses/{house_id}/floors/")
def add_floor(house_id: str, floor: Floor):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    floor.id = str(uuid.uuid4())
    houses[house_id].floors.append(floor)
    return floor

@app.delete("/houses/{house_id}/floors/{floor_id}")
def delete_floor(house_id: str, floor_id: str):
    house = houses.get(house_id)
    house.floors = [floor for floor in house.floors if floor.id != floor_id]
    return {"message": f"Floor {floor_id} deleted"}

# --- ROOM ENDPOINTS ---

@app.post("/houses/{house_id}/floors/{floor_id}/rooms/")
def add_room(house_id: str, floor_id: str, room: Room):
    house = houses.get(house_id)
    floor = next((f for f in house.floors if f.id == floor_id), None)
    room.id = str(uuid.uuid4())
    floor.rooms.append(room)
    return room

@app.delete("/houses/{house_id}/floors/{floor_id}/rooms/{room_id}")
def delete_room(house_id: str, floor_id: str, room_id: str):
    house = houses.get(house_id)
    floor = next((f for f in house.floors if f.id == floor_id), None)
    floor.rooms = [room for room in floor.rooms if room.id != room_id]
    return {"message": f"Room {room_id} deleted"}

# --- DEVICE ENDPOINTS ---

@app.post("/houses/{house_id}/floors/{floor_id}/rooms/{room_id}/devices/")
def add_device(house_id: str, floor_id: str, room_id: str, device: Device):
    house = houses.get(house_id)
    floor = next((f for f in house.floors if f.id == floor_id), None)
    room = next((r for r in floor.rooms if r.id == room_id), None)
    device.id = str(uuid.uuid4())
    room.devices.append(device)

    # Store latest device data in Redis
    redis_client.set(f"device:{device.id}:latest_data", str(device.data))

    return device

# --- REDIS: GET LATEST DEVICE DATA ---

@app.get("/devices/{device_id}/latest/")
def get_latest_device_data(device_id: str):
    data = redis_client.get(f"device:{device_id}:latest_data")
    if not data:
        raise HTTPException(status_code=404, detail="No cached data found for this device")
    return {"device_id": device_id, "latest_data": data, "source": "redis"}

# --- RUN LOCALLY ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
