from flask import Flask, app
from flask_socketio import SocketIO, send, emit
import socketio
from flask_cors import CORS, cross_origin
from backend.game_service.game_master import GameMaster
import json
from backend.game_service.game_master import Player

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app, cors_allowed_origins="*", mode="async")
cors = CORS(app)
game_master = GameMaster()

if __name__== '__main__':
    socketio.run(app)

# def application():
#     socketio.run(app)


# from flask import Flask
# from flask_socketio import SocketIO

# # socketio = SocketIO()


# def create_app(debug=False):
#     """Create an application."""
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'SECRET'
#     socketio = SocketIO(app, cors_allowed_origins="*", mode="async")
#     cors = CORS(app)
#     game_master = GameMaster()
#     return app, socketio