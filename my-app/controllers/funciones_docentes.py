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


def procesar_form_docente(tipo_doc, num_doc, nombres, apellidos,fecha_nacimiento, escolaridad, email, tel_fijo):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                sql = """
                INSERT INTO docente 
                (tipo_doc, num_doc, nombres, apellidos,fecha_nacimiento, escolaridad,  email, tel_fijo) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (tipo_doc, num_doc, nombres, apellidos,fecha_nacimiento, escolaridad,  email, tel_fijo)
                mycursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = mycursor.rowcount
                return resultado_insert
    except Exception as e:
        print(f"Error en el Insert Teacher: {e}")
        return []
    
def procesar_actualizacion_form_docente(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                tipo_doc = data.form['tipo_doc']
                num_doc = data.form['num_doc']
                nombres = data.form['nombres']
                apellidos = data.form['apellidos']
                fecha_nacimiento = data.form['fecha_nacimiento']
                escolaridad = data.form['escolaridad']                
                email = data.form['email']
                tel_fijo = data.form['tel_fijo']
                id_docente = data.form['id_docente']

                query_sql = """
                    UPDATE docente
                    SET 
                        tipo_doc = %s,
                        num_doc = %s,
                        nombres = %s,
                        apellidos = %s,
                        fecha_nacimiento = %s,
                        escolaridad = %s,
                        email = %s,
                        tel_fijo = %s                    
                    WHERE id_docente = %s
                """

                params = [
                    tipo_doc, num_doc, nombres, apellidos,fecha_nacimiento, escolaridad,  email, tel_fijo, id_docente
                ]

                cursor.execute(query_sql, params)
                conexion_MySQLdb.commit()
                print(f"Filas afectadas: {cursor.rowcount}")

        return cursor.rowcount
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_form_docente: {e}")
        return None
    
def buscarDocenteById(id_docente):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = "SELECT id_docente,tipo_doc, num_doc,nombres,apellidos,fecha_nacimiento,escolaridad, email,tel_fijo FROM docente  WHERE id_docente =%s LIMIT 1"
                    
                mycursor.execute(querySQL, (id_docente,))
                estudiante = mycursor.fetchone()
                return estudiante

    except Exception as e:
        print(f"Ocurrió un error en def buscarDocenteById: {e}")
        return []

 
# Lista de Docentes
def sql_lista_docentesBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT id_docente,tipo_doc, num_doc,nombres,apellidos,fecha_nacimiento,escolaridad, email,tel_fijo FROM docente"
                  
                cursor.execute(querySQL,)
                estudiantesBD = cursor.fetchall()
        return estudiantesBD
    except Exception as e:
        print(
            f"Error en la función sql_lista_docentesBD: {e}")
        return None
    
    
# Detalles del Docente
def sql_detalles_docentesBD(id_docente):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        e.id_docente,
                        e.tipo_doc, 
                        e.num_doc,
                        e.nombres,
                        e.apellidos,
                        e.fecha_nacimiento,
                        e.escolaridad,
                        e.email,
                        e.tel_fijo
                    FROM docente AS e
                    WHERE id_docente =%s
                    ORDER BY e.id_docente DESC
                    """)
                cursor.execute(querySQL, (id_docente,))
                estudiantesBD = cursor.fetchone()
        return estudiantesBD
    except Exception as e:
        print(
            f"Errro en la función sql_detalles_docentesBD: {e}")
        return None

    
# Eliminar Docente
def RemoverDocente(id_docente):
    try:
  
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM docente WHERE id_docente=%s"
                cursor.execute(querySQL, (id_docente,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarDocente : {e}")
        return []