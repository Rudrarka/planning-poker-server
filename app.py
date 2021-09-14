import json
from backend.game_service import game
from flask import Flask, app
from flask.globals import request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room
import socketio
from flask_cors import CORS
from backend.game_service.game_master import GameMaster
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
game_master = GameMaster()


@socketio.on('connect')
def handle_connect():
    """
    Handles connection request from clients 
    """
    sid = request.sid
    logging.info(f"connected to {sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """
    Handles disconnection from a client 
    """
    try:
        sid = request.sid
        updated_game = game_master.disconnect(sid)
        if updated_game:
            print(updated_game["id"])
            leave_room(updated_game["id"])
            emit('player_disconnected', updated_game, to=updated_game["id"])
    except Exception as e:
        logging.error(e)

@socketio.on('create_game')
def handle_create_game(game):
    """
    Creates a new game based on the game name 
    and the voting options. 
    """
    try:
        new_game = game_master.create_game(game)
        if new_game:
            emit('game_created', new_game)
    except Exception as e:
        logging.error(e)
        emit('game_creation_error', {"error": str(e)})

@socketio.on('player_join_request')
def handle_player_join_request(player_join_details):
    """
    Adds a player to an existing game. 
    """
    try:
        game_id = player_join_details["game_id"]
        game = game_master.join_game(player_join_details)
        join_room(game_id)
        emit('player_joined', game, to=game_id)
    except Exception as e:
        logging.error(e)
        emit('player_join_error', {"error": str(e)})

@socketio.on('create_player')
def handle_create_player(player):
    """
    Creates a player based on display name. 
    """
    try:
        sid = request.sid
        new_player = game_master.create_player(player, sid)
        game_master.add_lone_player(new_player)
        emit('player_created', new_player.toJSON())
    except Exception as e:
        logging.error(e)
        emit('player_create_error', {"error": str(e), "message":"Error in creating new player"})

@socketio.on('leave_game')
def handle_leave_game(leave_data):
    """
    Serves players request to leave the game. 
    """
    try:
        game_id = leave_data["game_id"]
        player_id = leave_data["player_id"]
        sid = request.sid
        updated_game = game_master.leave_game(game_id, sid)
        leave_room(game_id)
        emit('player_left', {"game":updated_game, "player_id":player_id}, to=game_id)
    except Exception as e:
        logging.error(e)
        emit('leave_game_error', {"error": str(e), "message":"Error in leaving game"})

@socketio.on('player_vote')
def handle_player_vote(vote_data):
    """
    Serves player's request to vote an option. 
    """
    try:
        game_id = vote_data["game_id"]
        updated_game = game_master.update_vote(vote_data)
        emit('player_voted', updated_game, to=game_id)
    except Exception as e:
        logging.error(e)
        emit('vote_error', {"error": str(e), "message":"Error in voting"})

@socketio.on('player_rejoin')
def handle_player_rejoin(player_data):
    """
    Serves player's request to rejoin a game. 
    """
    try:
        game_id = player_data["game_id"]
        sid = request.sid
        game = game_master.rejoin(player_data, sid)
        join_room(game_id)
        emit("player_joined", game, to=game_id)
    except Exception as e:
        logging.error(e)
        emit('player_join_error', {"error": str(e)})

@socketio.on('reset_game')
def handle_reset_game(game):
    """
    Serves player's request to reset the game. 
    """
    try:
        game_id = game["game_id"]
        updated_game = game_master.reset_game(game_id)
        socketio.emit("game_reset", updated_game, to=game_id)
    except Exception as e:
        logging.error(e)
        emit('reset_game_error', {"error": str(e), "message": "Error in resetting the game"})


@socketio.on('end_game')
def handle_end_game(game):
    """
    Serves player's request to end the game. 
    """
    try:
        game_id = game["game_id"]
        should_end = game_master.end_game(game_id)
        if should_end:
            socketio.emit("game_ended", to=game_id)
            close_room(game_id)
    except Exception as e:
        logging.error(e)
        emit('end_game_error', {"error": str(e), "message": "Error in ending the game"})
   

if __name__== '__main__':
    socketio.run(app, host="0.0.0.0")