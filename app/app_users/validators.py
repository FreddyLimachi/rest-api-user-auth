import re

def validate(username, email, password, confirm_pass, user, verify_email):

    if len(username) < 5 or len(username) > 15:
        return {'value': False, 'msg': 'El username debe contener entre a 5 a 15 carácteres'}


    elif re.match("^[a-zA-Z0-9_-]+$", username) is None:
        return {'value': False, 'msg': 'Unicos caracteres especiales permitidos: _ y -'}


    elif user and user['username'].lower() == username.lower():
        return {'value': False, 'msg': 'Ya existe el nombre de usuario'}


    elif validar_email(email) == False:
        return {'value': False, 'msg': 'Digite correctamente su email'}


    elif verify_email:
        return {'value': False, 'msg': 'El email ya esta siendo utilizado'}

    elif len(password) < 8:
        return {'value': False, 'msg': 'La contraseña debe contener al menos 8 carácteres'}

    elif password != confirm_pass:
        return {'value': False, 'msg': 'La contraseña de confirmación no coincide'}
    
    else: return True


def validar_email(correo):
    try:
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.match(expresion_regular, str(correo)) is not None
    except:
        False