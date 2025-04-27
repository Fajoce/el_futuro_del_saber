from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error
from conexion import conexionBD


# Importando cenexión a BD
from controllers.funciones_group import *

PATH_URL = "public/grupos"


@app.route('/registrar-grupo', methods=['GET'])
def viewFormGrupo():
    if 'conectado' in session:
        print('Listo')
        return render_template(f'{PATH_URL}/form_grupo.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/registrar-grupo')
def mostrar_docentes():
    if 'conectado' in session:    
         teachers = sql_lista_docentes()
         print("TEACHERS:", teachers) 
         return render_template(f'{PATH_URL}/form_grupo.html', teachers=teachers)
      
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/form-registrar-grupo', methods=['POST'])
def formGrupo():
    if 'conectado' in session:   
                 if request.method == 'POST' and 'grado' in request.form and 'id_docente' in request.form:
                    grado = request.form['grado']
                    id_docente = request.form['id_docente']
                    resultado = procesar_form_grupo(grado, id_docente)
                    if resultado:
                     return redirect(url_for('lista_grupos'))  
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-grupos', methods=['GET'])
def lista_grupos():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_grupos.html', grupos=sql_lista_grupo())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/borrar-grupo/<string:id_grupo>', methods=['GET'])
def borrarGrupo(id_grupo):
    resp = eliminarGrupo(id_grupo)
    if resp:
        flash('El Grupo fue eliminado correctamente', 'success')
        return redirect(url_for('lista_grupos'))