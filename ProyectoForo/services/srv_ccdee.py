import socket, json
from db_uci import dbuci
from comunicacion import sendT, listenB, registerS
srv = 'ccdee'

#Eliminar entidad
def eliE(opcion, rgtr):
    crsr = dbuci.cursor()
    fetched = None
    if opcion == 1:
        crsr.execute("DELETE FROM pasillo WHERE id_pasillo = %s", (rgtr,))
        dbuci.commit()
        response = {"respuesta":"El pasillo ha sido eliminado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 2:
        crsr.execute("DELETE FROM sala WHERE id_sala = %s", (rgtr,))
        dbuci.commit()
        response = {"respuesta":"La pieza ha sido eliminado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 3:
        crsr.execute("DELETE FROM personalLimpieza WHERE RUT = %s", (rgtr,))
        dbuci.commit()
        response = {"respuesta":"El empleado de limpieza ha sido eliminado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 4:
        crsr.execute("DELETE FROM paciente WHERE RUT = %s", (rgtr,))
        dbuci.commit()
        response = {"respuesta":"El paciente ha sido eliminado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 5:
        crsr.execute("DELETE FROM personalMedico WHERE RUT = %s", (rgtr,))
        dbuci.commit()
        response = {"respuesta":"El medico ha sido eliminado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 6:
        crsr.execute("DELETE FROM equipoMedico WHERE id_equipoMedico = %s", (rgtr,))
        dbuci.commit()
        response = {"respuesta":"La herramienta medica ha sido eliminada exitosamente."}
        sendT(sckt, srv, json.dumps(response))

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Servicio: Conectándose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except:
        print('No es posible la conexión al bus')
        quit()

    registerS(sckt, srv)

    while True:
        nS, mT = listenB(sckt)
        if nS == srv:
            mTloads = json.loads(mT)
            if mTloads["opcion"] == 1:
                eliE(opcion = mTloads["opcion"], rgtr = mTloads["id_pasillo"])
            elif mTloads["opcion"] == 2:
                eliE(opcion = mTloads["opcion"], rgtr = mTloads["id_sala"])
            elif mTloads["opcion"] == 3:
                eliE(opcion = mTloads["opcion"], rgtr = mTloads["RUT"])
            elif mTloads["opcion"] == 4:
                eliE(opcion = mTloads["opcion"], rgtr = mTloads["RUT"])
            elif mTloads["opcion"] == 5:
                eliE(opcion = mTloads["opcion"], rgtr = mTloads["RUT"])
            elif mTloads["opcion"] == 6:
                eliE(opcion = mTloads["opcion"], rgtr = mTloads["id_equipoMedico"])
        else:
            response = {"respuesta":"servicio incorrecto"}
            sendT(sckt, srv, json.dumps(response))

    print('Se cierra socket')
    sckt.close()