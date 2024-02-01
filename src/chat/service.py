from typing import Dict, List

from fastapi import WebSocket

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload
from src.chat.schema import CreateRoom, ResponseRoom, UserResponseRoom
from src.chat.model import Room
from src.user.model import User


class ChatService:
    def __init__(self) -> None:
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def get_room(self, session: AsyncSession, room_id: int) -> Room | None:
        room = await session.scalar(
            select(Room).where(Room.id == room_id)
            .options(selectinload(Room.users))
        )
        await session.commit()
        return room
    
    async def create_room(self, session: AsyncSession, 
                         create_room: CreateRoom,
                         user_id: int) -> Room:
        
        private = True if len(create_room.members) < 2 else False

        room = Room(
            name=create_room.name,
            private=private
        )

        session.add(room)
        
        user = await session.scalar(select(User).where(User.id == user_id)
                                    .options(selectinload(User.rooms)))
        user.rooms.append(room)

        for member_id in create_room.members:
            member = await session.scalar(select(User).where(User.id == member_id)
                                          .options(selectinload(User.rooms)))
            member.rooms.append(room)
        
        await session.commit()

        await session.refresh(room)
        id = room.id

        room = await self.get_room(session, id)

        return room

    async def start(self, websocket: WebSocket, session: AsyncSession, room_id: int) -> None:

        room = self.get_room(session, room_id)

        if not room:
            await websocket.close()
            return
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

        try:
            await websocket.accept()

            while True:
                # Receive message from the client
                message = await websocket.receive_text()

                # Construct the message data to be sent
                message_data = {
                    "room_id": room_id,
                    "message": message,
                }
                # json_message = json.dumps(message_data)

                # Broadcast the message to all connected websockets in the room
                for connection in self.active_connections[room_id]:
                    if connection != websocket:
                        await connection.send_text(message_data)

        except:
                pass
                

def get_chat_service() -> ChatService:
    return ChatService()