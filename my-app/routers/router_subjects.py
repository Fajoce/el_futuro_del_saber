from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error
from conexion import conexionBD


# Importando cenexión a BD
from controllers.funciones_subjects import *

PATH_URL = "public/asignaturas"


@app.route('/registrar-asignatura', methods=['GET'])
def viewFormAsignatura():
    if 'conectado' in session:
        print('Listo')
        return render_template(f'{PATH_URL}/form_asignatura.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-asignatura', methods=['POST'])
def formAsignatura():
   if 'conectado' in session:   
    if request.method == 'POST' and 'nombre' in request.form and 'id_docente' in request.form:
                    nombre = request.form['nombre']
                    id_docente = request.form['id_docente']
                    resultado = procesar_form_asignaturas(nombre, id_docente)
                    if resultado:
                     return redirect(url_for('lista_asignaturas'))  
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/lista-de-asignaturas', methods=['GET'])
def lista_asignaturas():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_asignaturas.html', asignaturas=sql_lista_asignaturasBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/borrar-asignatura/<string:id_asignatura>', methods=['GET'])
def borrarAsignatura(id_asignatura):
    resp = eliminarAsignatura(id_asignatura)
    if resp:
        flash('La asignatura fue eliminado correctamente', 'success')
        return redirect(url_for('lista_asignaturas'))