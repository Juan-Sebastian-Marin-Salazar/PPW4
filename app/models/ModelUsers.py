from .entities.users import User


class ModelUsers():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute(
                "call sp_verifyIdentity(%s, %s)",(user.email, user.password)
            )
            row = cursor.fetchone()
            if row[0] != None:
                user = User(row[0], row[1], row[2], row[4], row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id, email,usertype, fullname FROM users WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    
    @classmethod
    def get_by_email(self, db, email):
        cursor = db.connection.cursor()
        cursor.execute("SELECT fullname FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if(row != None):
            return True
        else:
            return False
    
    @classmethod
    def register(cls, db, user):
        try:
            cursor = db.connection.cursor()
        
        
            cursor.execute(
                "call sp_AddUser(%s,%s,%s,%s);", (user.email, user.password, user.fullname, user.usertype)
            )
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            print(f"Error en registro: {str(ex)}")  # Para debug
            return False
    
    
    @classmethod
    def update(cls, db, user):
        try:
            cursor = db.connection.cursor()
        
            cursor.execute(
                "call sp_UpdateUser(%s,%s,%s,%s);", (user.id ,user.email, user.password, user.fullname)
            )
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            print(f"Error en actualizacion: {str(ex)}")  # Para debug
            return False
        
    @classmethod
    def delete(cls, db, user):
        try:
            cursor = db.connection.cursor()
        
            cursor.execute(
                "DELETE FROM users WHERE id = %s;", (user.id,)
            )
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            print(f"Error en actualizacion: {str(ex)}")  # Para debug
            return False