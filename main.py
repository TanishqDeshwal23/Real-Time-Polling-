import asyncio
import sys
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from database import AsyncSessionLocal
from models import Poll, Choice

from sqlalchemy import select
from database import AsyncSessionLocal
from models import Poll

from sqlalchemy import select

# Windows compatibility
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )
    except Exception:
        pass

app = FastAPI(title="Real-Time Polling Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"Client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            if connection in self.active_connections:
                self.active_connections.remove(connection)


manager = ConnectionManager()

async def save_poll_to_db(question, options):

    try:

        async with AsyncSessionLocal() as session:

            poll = Poll(title=question)

            for option in options:
                poll.choices.append(
                    Choice(text=option)
                )

            session.add(poll)

            await session.commit()

            await session.refresh(poll)

            print("✅ Saved poll:", poll.id)

            return poll.id
        
        

    except Exception as e:

        print("❌ DATABASE ERROR:", e)

        raise
    
    
async def update_vote_in_db(poll_id, option_name):

    try:

        async with AsyncSessionLocal() as session:

            result = await session.execute(
                select(Choice).where(
                    Choice.poll_id == int(poll_id),
                    Choice.text == option_name
                )
            )

            choice = result.scalar_one_or_none()

            if choice:

                choice.votes += 1

                await session.commit()

                await session.refresh(choice)

                print(
                    f"✅ Vote Updated -> Poll:{poll_id}, "
                    f"Option:{option_name}, "
                    f"Votes:{choice.votes}"
                )

                return choice.votes

            return 0

    except Exception as e:

        print("❌ VOTE UPDATE ERROR:", e)

        return 0

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:

            data = await websocket.receive_text()
            raw_data = json.loads(data)

            print("Received:", raw_data)

            # CREATE POLL
            if raw_data.get("action") == "create_poll":
                print("Creating poll:", raw_data)

                poll_id = await save_poll_to_db(
                    raw_data.get("question"),
                    raw_data.get("options", [])
                )

                broadcast_payload = {
                    "type": "new_poll",
                    "data": {
                        "id":  str(poll_id),
                        "question": raw_data.get("question", "Live Poll"),
                        "options": {
                            opt: 0
                            for opt in raw_data.get("options", [])
                            if opt.strip()
                        }
                    }
                }

                await manager.broadcast(
                    json.dumps(broadcast_payload)
                )

            # VOTE
            elif raw_data.get("action") == "vote":

                poll_id = raw_data.get("poll_id")
                option_name = raw_data.get("option")

                updated_votes = await update_vote_in_db(
                    poll_id,
                    option_name
                )

                broadcast_payload = {
                    "type": "vote_update",
                    "poll_id": poll_id,
                    "option": option_name,
                    "votes": updated_votes
                }

                await manager.broadcast(
                    json.dumps(broadcast_payload)
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h2>⚡ Backend Operational. index.html missing.</h2>"


@app.get("/polls")
async def get_polls():

    async with AsyncSessionLocal() as session:

        result = await session.execute(
            select(Poll)
        )

        polls = result.scalars().all()

        response = []

        for poll in polls:

            response.append({
                "id": str(poll.id),
                "question": poll.title,
                "options": {
                    choice.text: choice.votes
                    for choice in poll.choices
                }
            })

        return response
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )