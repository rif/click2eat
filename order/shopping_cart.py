class ShoppingCart:
    def __init__(self, session, unit_id):
        self.order = {}
        for cart in [key for key in session.keys() if key.split(':',1)[0] == unit_id]:
            self.order[cart] = session[cart]
    
    def get_order(self):
        return self.order