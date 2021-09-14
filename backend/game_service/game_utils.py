def get_player_in_game_by_sid(game, sid):
        for p in game.players:
            if p.sid == sid: return p
                
def get_player_in_game(game, player_id):
        for p in game.players:
            if p.id == player_id: return p

def get_game_by_id(games, game_id):
        for g in games:
            if g.id == str(game_id): return g
                # return g
