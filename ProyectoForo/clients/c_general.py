import socket, json
from os import system, name
from comunicacion import clearS, sendT, listenB
rgtr = "ccdsu"  # Registro
lgin = "ccdli"  # Ingreso
gtdb = "ccddb"  # Consultar datos

sesion = {"username":None,"password":None,"rol":None}
sckt = None

def menuSULI():
    clearS()
    menu = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Elija una opción:                   *
    * 1) Sign up (Registrar un usuario)   *
    * 2) Log in (Ingresar con usuario)    *
    ***************************************

    Opción: """
    option = input(menu)
    if option == "1":
        menuSU()
    elif option =="2":
        menuLI()
    else:
        print("Opción ingresada no válida.")
        menuSULI()

def menuSU():
    username = None
    password = None
    rol = 2 # Usuario general
    clearS()

    menuUN = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """    
    clearS()
    username = input(menuUN)

    menuPW = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    clearS()
    password = input(menuPW)
    menuYN = f""""
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Registro de usuario                 *
    * Confirme sus datos [y/n]            *
    ***************************************
    
    Usuario: {username}
    Contraseña: {password}
    Rol: {"Administrador" if rol == "1" else "General"}
    
    Opción: """
    clearS()
    yn = input(menuYN)
    if yn == 'y':
        arg = {"username": username, "password": password, "rol": "2"}
        sendT(sckt, rgtr, json.dumps(arg))
        nS, msgT = listenB(sckt)
        msg = json.loads(msgT[12:])
        if nS == rgtr:
            if msg["respuesta"]:
                print(msg["respuesta"])
    else:
        menuSU()

def menuLI():
    username = None
    password = None
    #rol = 2 # Usuario general

    menuUN = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """   
    clearS()
    username = input(menuUN)

    menuPW = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    clearS()
    password = input(menuPW)

    arg = {"username": username, "password": password, "rol": 2}
    #arg = {"username": username, "password": password, "rol": rol}

    sendT(sckt, lgin, json.dumps(arg)) #Argumentos: socket, nombre del servicio, contenido que se envía
    
    nS, msgT=listenB(sckt) #Esto responde el bus nombre del servicio + mensaje de respuesta

    msg = json.loads(msgT[12:])
    if nS == lgin:
        if msg["respuesta"] == "No es posible entrar con el usuario ingresado.":
            input("No se ha podido iniciar sesión.")
            menuLI() 
        else:
            global sesion
            sesion=msg["respuesta"]
            if sesion["rol"] == 2:
                menuGD()
            else:
                menuLI()

def menuGD():
    menuGD2 = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Consultar datos                     *
    * Elija una opción                    *
    *-------------------------------------*
    * 1) Pasillos                         *
    * 2) Piezas                           *
    * 3) Camas                            *
    * 4) Pacientes                        *
    * 5) Personal Médico                  *
    * 6) Respiradores                     *
    *                                     *
    * 7) Cerrar sesión                    *
    ***************************************
    
    Opción: """
    opcion = int(input(menuGD2))
    if opcion == 7:
        #arg = {"username": None, "password": None, "rol": None}
        #sendT(sckt, lgin, json.dumps(arg))
        menuSULI()
    else:
        arg = {"opcion": opcion}
        sendT(sckt, gtdb, json.dumps(arg))
        nS, msgT = listenB(sckt)
        msg = msgT[12:]
        if nS == gtdb:
            if msg:
                print(msg)

                enter = input("Presione enter para continuar. ")
                clearS()
                menuGD()

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Cliente: Conectandose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except: 
        print('No es posible la conexión al bus')
        quit()

    menuSULI()