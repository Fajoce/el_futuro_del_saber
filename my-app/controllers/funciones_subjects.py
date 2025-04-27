# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string
import pdb
from conexion.conexionBD import connectionBD  # Conexión a BD

import datetime
import re
import os

from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio


import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file


def procesar_form_asignaturas(nombre, id_docente):

    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:

                sql = "INSERT INTO asignatura (nombre,id_docente) VALUES (%s, %s)"

                # Creando una tupla con los valores del INSERT
                valores = (nombre, id_docente)
                mycursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = mycursor.rowcount
                return resultado_insert
    except Exception as e:
            print(f"Error en el Insert Asignatura: {e}")
            return []


# Lista de Estudiantes
def sql_lista_asignaturasBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT a.id_asignatura, a.nombre, a.id_docente, CONCAT(d.nombres, ' ', d.apellidos) AS nombre_docente FROM asignatura a inner join docente d on d.id_docente = a.id_docente"
                  
                cursor.execute(querySQL,)
                asignaturasBD = cursor.fetchall()
        return asignaturasBD
    except Exception as e:
        print(
            f"Errro en la función sql_lista_asignaturasBD: {e}")
        return None
    
# Eliminar usuario
def eliminarAsignatura(id_asignatura):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM asignatura WHERE id_asignatura=%s"
                cursor.execute(querySQL, (id_asignatura,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarAsignatura : {e}")
        return []
