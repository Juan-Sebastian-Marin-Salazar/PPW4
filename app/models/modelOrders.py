from .entities.order import order

class ModelOrders:
    @classmethod
    def get_all_orders(db):
        cursor = db.connection.cursor()
        cursor.execute(
            "SELECT * FROM orders"
        )
        orders = cursor.fetchall()
        cursor.close()
        return orders

    @classmethod
    def get_not_delivered_orders(db):
        cursor = db.connection.cursor()
        cursor.execute(
            "SELECT * FROM orders WHERE delivered = FALSE"
        )
        orders = cursor.fetchall()
        cursor.close()
        return orders
    
    @classmethod
    def set_ordered_as_delivered(db, order):
        cursor = db.connection.cursor()
        cursor.execute(
            "UPDATE orders SET delivered = TRUE WHERE id = %s", (order.order_id,)
        )
        db.connection.commit()
        cursor.close()