class Player:
    """
    Holds information about the Player 
    """

    def __init__(self, id, name, is_admin, vote=None, sid=None) -> None:
        self.id = id
        self.name = name
        self.is_admin = is_admin
        self.vote = vote
        self.sid = sid

    def toJSON(self):
        """
        Helper function to return json object 
        """
        return {
                'id':self.id,
                'name': self.name,
                'is_admin': self.is_admin,
                'vote': self.vote
            }
