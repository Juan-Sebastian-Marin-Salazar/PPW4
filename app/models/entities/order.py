class order:
    def __init__(self, order_id, ownerid, order_date, cost, delivered) -> None:
        self.order_id = order_id
        self.ownerid = ownerid
        self.order_date = order_date
        self.cost = cost
        self.delivered = delivered