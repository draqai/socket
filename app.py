# app.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Basic route to confirm the server is running
@app.route('/')
def index():
    return jsonify({"status": "Socket.IO server is running"})

# Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)
    socketio.emit('welcome', {'message': 'Welcome to the server!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    # Broadcast the message to all clients
    socketio.emit('message', {'sender': request.sid, 'data': data})

# You can add more custom events
@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    if room:
        from flask_socketio import join_room
        join_room(room)
        socketio.emit('room_joined', {'room': room}, room=room)

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    
    # Use debug mode based on environment
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Start the Socket.IO server
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
