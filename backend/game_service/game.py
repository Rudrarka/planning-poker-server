import json
from enum import Enum

class GameOptions(Enum):
  """
  Mapping from API enum name to database id for StdTestRole
  """
  simple = [1.5,2,3,4,5,6,7,8,9,10]
  fibonacci = [1, 2, 3, 5, 8, 13, 21]

class Game:
    """
    Holds information about the Game
    """

    def __init__(self, id, name, options=None) -> None:
        self.id = id
        self.name = name
        self.players = []
        self.options = GameOptions[options].value if options else None

    def toJSON(self):
        """
        Helper function to return json
        """
        return {
            'id':self.id,
            'name': self.name,
            'players': [p.toJSON() for p in self.players],
            'options': self.options
        }