from .entities.order import order

class ModelOrders:
    @classmethod
    def get_all_orders(cls,db):
        cursor = db.connection.cursor()
        cursor.execute(
            "SELECT * FROM orders"
        )
        orders = cursor.fetchall()
        cursor.close()
        return orders

    @classmethod
    def get_not_delivered_orders(cls,db):
        cursor = db.connection.cursor()
        cursor.execute(
            "SELECT * FROM orders WHERE delivered = FALSE"
        )
        orders = cursor.fetchall()
        cursor.close()
        return orders
    
    @classmethod
    def set_ordered_as_delivered(cls, db, order_id):
        cursor = db.connection.cursor()
        try:
            cursor.execute(
                "UPDATE orders SET delivered = TRUE WHERE order_id = %s", (order_id,)
            )
            db.connection.commit()
        except Exception as e:
            db.connection.rollback()
            raise e
        finally:
            cursor.close()