from fastapi import Security, WebSocket, WebSocketDisconnect, WebSocketException, APIRouter, Depends, Request
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.security import check_access_token
from src.database import get_async_session
from src.chat.service import get_chat_service, ChatService
from src.chat.schema import CreateRoom, ResponseRoom, UserResponseRoom
from src.chat.model import Room

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    dependencies=[Security(check_access_token)]
)


@router.post("/room", response_model=ResponseRoom)
async def create_room(create_room: CreateRoom,
                      request: Request,
                      session: AsyncSession = Depends(get_async_session),
                      service: ChatService = Depends(get_chat_service)):
    
    user_id = request.state.user.id

    room = await service.create_room(session, create_room, user_id)
    res = ResponseRoom(**room.__dict__, 
                        members=[UserResponseRoom(**user.__dict__) for user in room.users])
    return res

@router.get("/room/{room_id}", response_model=ResponseRoom)
async def get_room(room_id: int,
                   session: AsyncSession = Depends(get_async_session),
                   service: ChatService = Depends(get_chat_service)):
    
    room = await service.get_room(session, room_id)

    response_room = ResponseRoom(**room.__dict__,
                                 members=[UserResponseRoom(**user.__dict__) for user in room.users])

    return response_room



# @router.websocket("/messages/{room_id}", dependencies=Security(check_access_token))
# async def websocket_endpoint(room_id: int, 
#                              websocket: WebSocket,
#                              session: Depends(get_async_session),
#                              service: Depends(get_chat_service)):
  
#   db = database.SessionLocal()
#   room = crud.get_room(db, room_id)
#   db.close()
#   if not room:
#       await websocket.close()
#       return

#   # Add the websocket connection to the active connections for the room
#   if room_id not in active_connections:
#       active_connections[room_id] = []
#   active_connections[room_id].append(websocket)

#   try:
#       await websocket.accept()

#       while True:
#           # Receive message from the client
#           message = await websocket.receive_text()

#           # Construct the message data to be sent
#           message_data = {
#               "room_id": room_id,
#               "message": message,
#           }
#           json_message = json.dumps(message_data)

#           # Broadcast the message to all connected websockets in the room
#           for connection in active_connections[room_id]:
#             if connection != websocket:
#               await connection.send_text(json_message)

#   except:
#         pass

