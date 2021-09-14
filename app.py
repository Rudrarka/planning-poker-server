import json
from backend.game_service import game
from flask import Flask, app
from flask.globals import request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room
import socketio
from flask_cors import CORS
from backend.game_service.game_master import GameMaster

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
game_master = GameMaster()

@socketio.on('create_game')
def handle_create_game(game):
    try:
        new_game = game_master.create_game(game)
        print(new_game)
        if new_game:
            emit('game_created', new_game)
    except Exception as e:
        print(e)
        emit('game_created', {"error": e})

@socketio.on('player_join_request')
def handle_player_join_request(player_join_details):
    try:
        print('player_join_request')
        game_id = player_join_details["game_id"]
        game = game_master.join_game(player_join_details)
        join_room(game_id)
        emit('player_joined', game, to=game_id)
    except Exception as e:
        print(e)
        emit('player_join_error', {"error": str(e)})

@socketio.on('create_player')
def handle_create_player(player):
    try:
        sid = request.sid
        new_player = game_master.create_player(player, sid)
        game_master.add_lone_player(new_player)
        print(new_player.toJSON())
        # emit('player_created', json.dumps(new_player.__dict__))
        emit('player_created', new_player.toJSON())
    except Exception as e:
        emit('player_create_error', {"error": str(e), "message":"Error in creating new player"})

@socketio.on('leave_game')
def handle_leave_game(leave_data):
    try:
        game_id = leave_data["game_id"]
        player_id = leave_data["player_id"]
        sid = request.sid
        updated_game = game_master.leave_game(game_id, sid)
        leave_room(game_id)
        emit('player_left', {"game":updated_game, "player_id":player_id}, to=game_id)
    except Exception as e:
        pass

@socketio.on('player_vote')
def handle_player_vote(vote_data):
    try:
        game_id = vote_data["game_id"]
        updated_game = game_master.update_vote(vote_data)
        emit('player_voted', updated_game, to=game_id)
    except Exception as e:
        pass

@socketio.on('player_rejoin')
def handle_player_rejoin(player_data):
    try:
        game_id = player_data["game_id"]
        sid = request.sid
        game = game_master.rejoin(player_data, sid)
        join_room(game_id)
        print(game)
        emit("player_joined", game, to=game_id)
    except Exception as e:
        emit('player_join_error', {"error": str(e)})

@socketio.on('reset_game')
def handle_reset_game(game):
   game_id = game["game_id"]
   updated_game = game_master.reset_game(game_id)
   socketio.emit("game_reset", updated_game, to=game_id)

@socketio.on('end_game')
def handle_end_game(game):
   game_id = game["game_id"]
   should_end = game_master.end_game(game_id)
   if should_end:
    socketio.emit("game_ended", to=game_id)
    close_room(game_id)
   

@socketio.on('connect')
def handle_connect():
   print('connected')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'disconnected')
    try:
        sid = request.sid
        updated_game = game_master.disconnect(sid)
        if updated_game:
            leave_room(updated_game["id"])
            emit('player_disconnected', updated_game, to=updated_game["id"])
    except Exception as e:
        print(e)

if __name__== '__main__':
    socketio.run(app, host="0.0.0.0")