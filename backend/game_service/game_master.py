from .player import Player
from .game import Game
import uuid
from .game_utils import get_player_in_game_by_sid, get_player_in_game, get_game_by_id
from backend.game_service import game_utils

class GameMaster:

    def __init__(self):
        self.games = []
        self.lone_players =[]

    def create_game(self, game):
        game_present = any(g.name == str(game["name"]) for g in self.games)
        # can_create =  (name != g.name for g in self.games) 
        if not game_present:
            game = Game(str(uuid.uuid1()), game["name"], game["option"])
            print(game)
            self.games.append(game)
            return game.toJSON()
    
    # def view_games(self):
    #     return [g.name for g in self.games]

    def create_player(self, player_data, sid, new=True):
        print('in create player')
        if new:
            player = Player(str(uuid.uuid1()), player_data["display_name"], player_data["is_admin"], sid)
        else:
            player = Player(str(player_data["id"]), player_data["name"], player_data["is_admin"], player_data["vote"], sid)
        return player

    # def get_game_by_id(self, game_id):
    #     for g in self.games:
    #         if g.id == str(game_id):
    #             return g

    def join_game(self, player_join_details):
        game = game_utils.get_game_by_id(self.games, str(player_join_details["game_id"]))
        if not game:
            raise Exception("No game available")
        for lone_player in self.lone_players:
            if str(lone_player.id) == player_join_details["player_id"]:
                game.players.append(lone_player)
                break
        self.lone_players.remove(lone_player)
        return game.toJSON()

    def add_lone_player(self, player):
        self.lone_players.append(player)
    
    def leave_game(self, game_id, sid):
        game = game_utils.get_game_by_id(self.games, game_id)
        player = None
        if not game:
            raise Exception(f"No game available with id {game_id}")
        player = game_utils.get_player_in_game_by_sid(game, sid)
        if player:
            game.players.remove(player)
        return game.toJSON()

    def update_vote(self, vote_data):
        game = game_utils.get_game_by_id(self.games, vote_data["game_id"])
        if not game:
            raise Exception("No game available")
        player = game_utils.get_player_in_game(game, vote_data["player_id"])
        print(player)
        if player:
            player.vote = vote_data["vote"]
            return game.toJSON()

    def rejoin(self, player_data, sid):
        print('in rejoin')
        game = game_utils.get_game_by_id(self.games, player_data["game_id"])
        if not game:
            raise Exception("No game available")
        player = game_utils.get_player_in_game(game, player_data["id"])
        if not player:
            player = self.create_player(player_data, sid, new=False)
            print(game)
            game.players.append(player)
        else:
            player.sid = sid        
        return game.toJSON()

    def find_player_by_sid(self, sid):
        print('in find_player_by_sid')
        for g in self.games:
            return g, game_utils.get_player_in_game_by_sid(g, sid)

    def disconnect(self, sid):
        game, player = self.find_player_by_sid(sid)
        if player and game:
            game.players.remove(player)
            return game.toJSON()
    
    def reset_game(self, game_id):
        game = game_utils.get_game_by_id(self.games, game_id)
        if not game:
            raise Exception("No game available")
        for player in game.players: player.vote = None
        return game.toJSON()
    
    def end_game(self, game_id):
        game = game_utils.get_game_by_id(self.games, game_id)
        if not game:
            raise Exception("No game available")
        self.games.remove(game)
        return True
         
            



    