import socket, json
from db_uci import dbuci
from comunicacion import sendT, listenB, registerS
srv = 'ccdae'

#Agregar entidad
def addE(opcion, rgtr):
    crsr = dbuci.cursor()
    fetched = None
    if opcion == 1:
        crsr.execute("INSERT INTO pasillo (estado) VALUES (%s)", (rgtr[0],))
        dbuci.commit()
        response = {"respuesta":"El pasillo ha sido ingresado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 2:
        crsr.execute("INSERT INTO sala (id_sala, cantCamas, camasDisp, estado) VALUES (%s, %s, %s, %s)", (rgtr[0], rgtr[1], rgtr[1], rgtr[2]))
        dbuci.commit()
        response = {"respuesta":"La pieza ha sido ingresada exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 3:
        crsr.execute("INSERT INTO personalLimpieza (RUT, nombre, fechaNac, disponible) VALUES (%s, %s, %s, %s)", (rgtr[0], rgtr[1], rgtr[2], 1))
        dbuci.commit()
        response = {"respuesta":"El empleado de limpieza ha sido ingresado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 4:
        crsr.execute("INSERT INTO paciente (RUT, nombre, fechanac, edad, enfermedad, sintomas, dieta, alergias, medicamentos, tratamiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (rgtr[0], rgtr[1], rgtr[2], rgtr[3], rgtr[4], rgtr[5], rgtr[6], rgtr[7], rgtr[8], rgtr[9]))
        dbuci.commit()
        response = {"respuesta":"El paciente ha sido ingresado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 5:
        crsr.execute("INSERT INTO personalMedico (RUT, nombre, fechanac, especialidad, disponible) VALUES (%s, %s, %s, %s, %s)", (rgtr[0], rgtr[1], rgtr[2], rgtr[3], rgtr[4]))
        dbuci.commit()
        response = {"respuesta":"El medico ha sido ingresado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 6:
        crsr.execute("INSERT INTO equipoMedico (u_paciente_RUT, tipo, fechaInicio, tiempoUso, estado) VALUES(%s, %s, %s, %s, %s)", (rgtr[0], rgtr[1], rgtr[2], rgtr[3], rgtr[4]))
        dbuci.commit()
        response = {"respuesta":"La herramienta medica ha sido ingresada exitosamente."}
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
            l = []
            mTloads = json.loads(mT)
            if mTloads["opcion"] == 1:
                l.append(mTloads["estado"])
            elif mTloads["opcion"] == 2:
                l.append(mTloads["id_sala"])
                l.append(mTloads["cantCamas"])
                l.append(mTloads["estado"])
            elif mTloads["opcion"] == 3:
                l.append(mTloads["RUT"])
                l.append(mTloads["nombre"])
                l.append(mTloads["fechaNac"])
                l.append(mTloads["disponible"])
            elif mTloads["opcion"] == 4:
                l.append(mTloads["RUT"])
                l.append(mTloads["nombre"])
                l.append(mTloads["fechanac"])
                l.append(mTloads["edad"])
                l.append(mTloads["enfermedad"])
                l.append(mTloads["sintomas"])
                l.append(mTloads["dieta"])
                l.append(mTloads["alergias"])
                l.append(mTloads["medicamentos"])
                l.append(mTloads["tratamiento"])
            elif mTloads["opcion"] == 5:
                l.append(mTloads["RUT"])
                l.append(mTloads["nombre"])
                l.append(mTloads["fechanac"])
                l.append(mTloads["especialidad"])
                l.append(mTloads["disponible"])
            elif mTloads["opcion"] == 6:
                l.append(mTloads["u_paciente_RUT"])
                l.append(mTloads["tipo"])
                l.append(mTloads["fechaInicio"])
                l.append(mTloads["tiempoUso"])
                l.append(mTloads["estado"])
            addE(opcion = mTloads["opcion"], rgtr = l)
        else:
            response = {"respuesta":"servicio incorrecto"}
            sendT(sckt, srv, json.dumps(response))

    print('Se cierra socket')
    sckt.close()