import logging
from .player import Player
from .game import Game
import uuid
from backend.game_service import game_utils

class GameMaster:
    """
    Game master/controller who controls and stores all actions of a Game
    """

    def __init__(self):
        self.games = []
        self.lone_players =[]

    def create_game(self, game):
        """
        Creates a game 
        """
        game_present = any(g.name == str(game["name"]) for g in self.games)
        if not game_present:
            game = Game(str(uuid.uuid1()), game["name"], game["option"])
            self.games.append(game)
            logging.info(f"Created game with id {game.id}")
            return game.toJSON()
    
    def create_player(self, player_data, sid, new=True):
        """
        Creates a player 
        """
        if new:
            player = Player(str(uuid.uuid1()), player_data["display_name"], player_data["is_admin"], sid)
        else:
            player = Player(str(player_data["id"]), player_data["name"], player_data["is_admin"], player_data["vote"], sid)
        logging.info(f"Created player with id {player.id}")
        return player

    def join_game(self, player_join_details):
        """
        Player joins a game 
        """
        game = game_utils.get_game_by_id(self.games, str(player_join_details["game_id"]))
        if not game:
            raise Exception("No game available")
        for lone_player in self.lone_players:
            if str(lone_player.id) == player_join_details["player_id"]:
                game.players.append(lone_player)
                logging.info(f"Player with id {lone_player.id} joined a game with id {game.id}")
                break
        self.lone_players.remove(lone_player)
        return game.toJSON()

    def add_lone_player(self, player):
        """
        Adds a player who is not in any game in the lone player list 
        """
        self.lone_players.append(player)
        logging.info(f"Player with id {player.id} is not associated with any game")
    
    def leave_game(self, game_id, sid):
        """
        Facilitates player's request to leave a game 
        """
        game = game_utils.get_game_by_id(self.games, game_id)
        player = None
        if not game:
            raise Exception(f"No game available with id {game_id}")
        player = game_utils.get_player_in_game_by_sid(game, sid)
        if player:
            game.players.remove(player)
            logging.info(f"Player {player.id} left game {game.id}")
        return game.toJSON()

    def update_vote(self, vote_data):
        """
        Updates vote status of a game. 
        """
        game = game_utils.get_game_by_id(self.games, vote_data["game_id"])
        if not game:
            raise Exception("No game available")
        player = game_utils.get_player_in_game(game, vote_data["player_id"])
        if player:
            player.vote = vote_data["vote"]
            logging.info(f"Player {player.id} voted for {player.vote} in game {game.id}")
            return game.toJSON()

    def rejoin(self, player_data, sid):
        """
        Rejoins a player in a game. 
        """
        game = game_utils.get_game_by_id(self.games, player_data["game_id"])
        if not game:
            raise Exception("No game available")
        player = game_utils.get_player_in_game(game, player_data["id"])
        if not player:
            player = self.create_player(player_data, sid, new=False)
            game.players.append(player)
        else:
            player.sid = sid
        logging.info(f"Player {player.id} joined the game {game.id}")        
        return game.toJSON()

    def disconnect(self, sid):
        """
        Handles client disconnection
        """
        game, player = game_utils.find_player_by_sid(self.games, sid)
        if player and game:
            game.players.remove(player)
            logging.info(f"Player {player.id} disconnected")
            return game.toJSON()
    
    def reset_game(self, game_id):
        """
        Resets a game
        """
        game = game_utils.get_game_by_id(self.games, game_id)
        if not game:
            raise Exception("No game available")
        for player in game.players: player.vote = None
        logging.info(f"Game {game.id} reset")
        return game.toJSON()
    
    def end_game(self, game_id):
        """
        Ends a game
        """
        game = game_utils.get_game_by_id(self.games, game_id)
        if not game:
            raise Exception("No game available")
        self.games.remove(game)
        logging.info(f"Game {game.id} ended")
        return True
         
            



    