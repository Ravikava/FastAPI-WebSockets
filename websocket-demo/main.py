from fastapi import FastAPI, WebSocket
from typing import Dict, List
from asyncio import sleep,create_task
from fastapi_socketio import SocketManager
import socketio,asyncio

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
app = socketio.ASGIApp(sio, app)



rooms: Dict[str, Dict[int, WebSocket]] = {}
chat_history: Dict[str, Dict[int, List[str]]] = {}


# @app.websocket("/ws/{room_id}/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: int):
#     print(f"\n\n\n websocket {websocket} \n\n\n")
#     await websocket.accept()

#     if room_id not in rooms:
#         rooms[room_id] = {}
#         chat_history[room_id] = {}

#     rooms[room_id][user_id] = websocket

#     print(f"user id in room {rooms[room_id][user_id]} \n\n rooms {rooms}")
#     # Check if the user already has a chat history in the room
#     if user_id not in chat_history[room_id]:
#         chat_history[room_id][user_id] = []

#     try:
#         # Send chat history to the user
#         await websocket.send_text("Chat History:\n" + "\n".join(chat_history[room_id][user_id]))

#         while True:
#             data = await websocket.receive_text()

#             # Append the message to the chat history
#             chat_history[room_id][user_id].append(f"User {user_id}: {data}")

#             # Broadcast the message to all users in the room except the sender
#             for other_user_id, other_user_connection in rooms[room_id].items():
#                 if other_user_id != user_id:
#                     await other_user_connection.send_text(f"User {user_id}: {data}")
#     except Exception as e:
#         print(e)
        
# connections: Dict[int, WebSocket] = {}
# import asyncio
        
# @app.websocket("/ws/get_timer/{user_id}/")
# async def websocket_endpoint(websocket: WebSocket, user_id: int):
#     print('stage 1')
#     try:
#         await websocket.accept()
#         print('stage 1')
#         connections[user_id] = websocket
#         countdown_seconds = 60  # 15 minutes = 900 seconds
#         print('stage 2')
#         while countdown_seconds > 0:
#             print('stage 3')
#             # Send countdown message to the user
            
#             await websocket.send_text(f"Countdown: {countdown_seconds}")
#             # print(f"Countdown: {minutes:02d}:{seconds:02d}")
#             countdown_seconds -= 1
#             await asyncio.sleep(1)
#     except Exception as e:
#         print(e)
        
        
# connected_clients = set()

# async def countdown_timer():
#     for i in range(900, 0, -1):  # 15 minutes = 900 seconds
#         minutes = i // 60
#         seconds = i % 60
#         countdown_str = f"{minutes:02d}:{seconds:02d}"
        
#         for client in connected_clients:
#             await client.send_text(f"Time left: {countdown_str}")
        
#         await sleep(1)
        
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     connected_clients.add(websocket)
#     try:
#         while True:
#             await websocket.receive_text()
#     except:
#         connected_clients.remove(websocket)

# @app.on_event("startup")
# async def startup_event():
#     create_task(countdown_timer())
    
@sio.on('chat_message')
async def handle_chat_message(sid, data):
    await sio.emit('chat message', data, room=sid)

@sio.on('start_countdown')
async def handle_start_countdown(sid,data):
    for i in range(900, 0, -1):
        minutes = i // 601
        seconds = i % 60
        await sio.emit('countdown', f"{minutes:02d}:{seconds:02d}")
        
        await asyncio.sleep(1)
        
@sio.on('booking_requests')
async def booking_requests(sid,data):
    try:
        print(f"\n\n\n booking_requests emited \n\n\n")
        import random
        await asyncio.sleep(60)
        for i in range(1,11):
            temp = {
                'price': random.randint(99, 9999),
                'vehicle_type':'SUV',
                'vehicle_details':{
                        'vehicle_name' : 'Harrier',
                        'vehicle_number' : 'GJ01AA1234',
                        'vehicle_type' : 'SUV',
                        'vehicle_model' : '',
                        'vehicle_color' : 'Black',
                        'vehicle_chesis_no' : 'az123asd1234',
                        
                    },
                'vehicle_images' : [
                        'https://imgd.aeplcdn.com/640X480/cw/ucp/stockApiImg/LZ3RR8V_0db0147e9fb64cb492e3de8d516f0343_1_38782307.jpg?q=80',
                        'https://imgd.aeplcdn.com/640X480/cw/ucp/stockApiImg/JJA13XY_0db0147e9fb64cb492e3de8d516f0343_1_38782308.jpg?q=80',
                        'https://imgd.aeplcdn.com/640X480/cw/ucp/stockApiImg/56VZ588_0db0147e9fb64cb492e3de8d516f0343_1_38782310.jpg?q=80',
                        'https://imgd.aeplcdn.com/640X480/cw/ucp/stockApiImg/BDI9HZ1_0db0147e9fb64cb492e3de8d516f0343_1_38782311.jpg?q=80'
                    ],
                'trip_details' : {
                    'dummy' : 'data'
                }
            }
            await sio.emit('get_booking_requests',temp)
            
            await asyncio.sleep(random.randint(5, 61))
        print(f"\n\n\n get_booking_requests emited \n\n\n")
    except Exception as e:
        print(f"\n\n\n booking_requests Error : {str(e)} \n\n\n")
        
    
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.29.131", port=8000)