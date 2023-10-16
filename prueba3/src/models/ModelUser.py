import datetime
import secrets

from .entities.User import User


class ModelUser():

    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            # Asegúrate de seleccionar el token y su tiempo de generación del usuario
            sql = "SELECT id, username, fullname, token, token_timestamp FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                # Devuelve el token y su tiempo de generación del usuario
                return User(row[0], row[1], None, row[2], row[3], row[4])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


# Esta función genera un nuevo token de 6 dígitos
def generate_new_token():
    new_token = secrets.token_hex(3)  # Genera un token hexadecimal de 6 caracteres
    return new_token

# Esta función actualiza el token y su tiempo de generación en la base de datos
def update_token_in_database(new_token, user_id, db):
    try:
        cursor = db.connection.cursor()
        # Almacena el token y el tiempo actual en la base de datos
        sql = "UPDATE user SET token = %s, token_timestamp = %s WHERE id = %s"
        cursor.execute(sql, (new_token, datetime.datetime.now(), user_id))
        db.connection.commit()
        return True
    except Exception as ex:
        raise Exception(ex)