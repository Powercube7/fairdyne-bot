"""
Server for handling shield direction updates via WebSocket.
The server bridges communication between 2 clients: the Python script and the game engine.

Author: Powercube
"""
from flask import Flask
from flask_socketio import SocketIO
from socketio import Client
from tools import Directions

def send_direction(direction: Directions, client: Client):
    if not client.connected:
        client.connect("http://localhost:5000")

    client.emit("shield_update", {
        "direction": direction.name,
        "angle": direction.angle,
        "input_key": direction.input_key,
        "shield_direction": direction.shield_direction
    })

if __name__ == "__main__":
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*", monitor_clients=False)

    @socketio.on("connect")
    def handle_connect():
        print("Client connected")

    @socketio.on("disconnect")
    def handle_disconnect():
        print("Client disconnected")

    @socketio.on("shield_update")
    def handle_shield_update(data):
        print("Shield update received:", data)
        socketio.emit("shield_update", data) # Broadcast shield update to all connected clients

    socketio.run(app, port=5000)
