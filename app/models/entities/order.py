class order:
    def __init__(self, id, ownerid, date, cost, delivered) -> None:
        self.id = id
        self.ownerid = ownerid
        self.date = date
        self.cost = cost
        self.delivered = delivered