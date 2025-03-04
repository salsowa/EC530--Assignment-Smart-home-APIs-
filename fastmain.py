from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI()

# In-memory database (temporary storage)
users = {}
houses = {}

# Data Models
class Metadata(BaseModel):
    description: Optional[str] = None
    location: Optional[str] = None

class Device(BaseModel):
    name: str
    type: str
    data: dict

class Room(BaseModel):
    name: str
    metadata: Optional[Metadata] = None
    devices: List[Device] = []

class House(BaseModel):
    name: str
    metadata: Optional[Metadata] = None
    rooms: List[Room] = []

class User(BaseModel):
    name: str
    email: str

# --- USER ROUTES ---

@app.post("/users/")
def create_user(user: User):
    user_id = str(uuid.uuid4())
    users[user_id] = {"id": user_id, "name": user.name, "email": user.email}
    return users[user_id]

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: str, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id].update({"name": user.name, "email": user.email})
    return users[user_id]

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"message": f"User {user_id} deleted"}

# --- HOUSE ROUTES ---

@app.post("/houses/")
def create_house(house: House):
    house_id = str(uuid.uuid4())
    houses[house_id] = {"id": house_id, **house.dict()}
    return houses[house_id]

@app.get("/houses/{house_id}")
def get_house(house_id: str):
    house = houses.get(house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return house

@app.put("/houses/{house_id}")
def update_house(house_id: str, house: House):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    houses[house_id].update(house.dict())
    return houses[house_id]

@app.delete("/houses/{house_id}")
def delete_house(house_id: str):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    del houses[house_id]
    return {"message": f"House {house_id} deleted"}

# --- ROOM ROUTES ---

@app.post("/houses/{house_id}/rooms/")
def add_room(house_id: str, room: Room):
    house = houses.get(house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    room_id = str(uuid.uuid4())
    if "rooms" not in house:
        house["rooms"] = []

    house["rooms"].append({"id": room_id, **room.dict()})
    return house["rooms"][-1]

@app.delete("/houses/{house_id}/rooms/{room_id}")
def delete_room(house_id: str, room_id: str):
    house = houses.get(house_id)
    if not house or "rooms" not in house:
        raise HTTPException(status_code=404, detail="House or rooms not found")

    house["rooms"] = [room for room in house["rooms"] if room["id"] != room_id]
    return {"message": f"Room {room_id} deleted"}

# --- DEVICE ROUTES ---

@app.post("/houses/{house_id}/rooms/{room_id}/devices/")
def add_device(house_id: str, room_id: str, device: Device):
    house = houses.get(house_id)
    if not house or "rooms" not in house:
        raise HTTPException(status_code=404, detail="House or rooms not found")

    room = next((r for r in house["rooms"] if r["id"] == room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    device_id = str(uuid.uuid4())
    if "devices" not in room:
        room["devices"] = []

    room["devices"].append({"id": device_id, **device.dict()})
    return room["devices"][-1]

# Run FastAPI with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
