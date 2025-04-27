from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error
from conexion import conexionBD


# Importando cenexión a BD
from controllers.funciones_docentes import *

PATH_URL = "public/docentes"


@app.route('/registrar-docente', methods=['GET'])
def viewFormDocente():
    if 'conectado' in session:
        print('Listo')
        return render_template(f'{PATH_URL}/form_docente.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    

@app.route('/form-registrar-docente', methods=['POST'])
def formDocente():
    if 'conectado' in session:   
                if request.method == 'POST' and 'tipo_doc' in request.form and 'num_doc' in request.form  and 'nombres' in request.form and 'apellidos' in request.form and 'fecha_nacimiento' in request.form and 'escolaridad' in request.form  and 'email' in request.form and 'tel_fijo' in request.form:
                    tipo_doc = request.form['tipo_doc']
                    num_doc = request.form['num_doc']
                    nombres = request.form['nombres']
                    apellidos = request.form['apellidos']
                    fecha_nacimiento = request.form['fecha_nacimiento']
                    escolaridad = request.form['escolaridad']
                    email = request.form['email']
                    tel_fijo = request.form['tel_fijo']

                    resultado = procesar_form_docente(tipo_doc, num_doc, nombres, apellidos,fecha_nacimiento, escolaridad, email, tel_fijo)
                    if resultado:
                     return redirect(url_for('lista_docentes'))  
                    else:
                     flash('primero debes iniciar sesión.', 'error')
                     return redirect(url_for('inicio'))
                    
@app.route("/detalles-docente/", methods=['GET'])
@app.route("/detalles-docente/<int:id_docente>", methods=['GET'])
def detalleDocente(id_docente=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEstudiante es None o no está presente en la URL
        if id_docente is None:
            return redirect(url_for('inicio'))
        else:
            detalle_docente = sql_detalles_docentesBD(id_docente) or []
            return render_template(f'{PATH_URL}/detalles_docente.html', detalle_docente=detalle_docente)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/editar-docente/<string:id_docente>', methods=['GET'])
def viewEditarDocente(id_docente):
    if 'conectado' in session:
        respuestaDocente = buscarDocenteById(id_docente)
        if respuestaDocente:
            return render_template(f'{PATH_URL}/form_docente_update.html', respuestaDocente=respuestaDocente)
        else:
            flash('El docente no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion del docente
@app.route('/actualizar-docente', methods=['POST'])
def actualizarDocente():
    try: 
        resultData = procesar_actualizacion_form_docente(request)
        if resultData:
            flash('Docente actualizado correctamente.', 'success')
        else:
            flash('No se pudo actualizar el docente.', 'error')
        return redirect(url_for('lista_docentes'))
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash('Error inesperado al actualizar docente.', 'error')
        return redirect(url_for('lista_docentes'))

@app.route('/lista-de-docentes', methods=['GET'])
def lista_docentes():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_docentes.html', docentes=sql_lista_docentesBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/borrar-docente/<string:id_docente>', methods=['GET'])
def borrarDocente(id_docente):          
        try:
            resp = RemoverDocente(id_docente)
            if resp:
             flash('El Docente fue eliminado correctamente', 'success')
            return redirect(url_for('lista_docentes'))
        except Exception as e:
         flash(f"Error en eliminarDocente : {e}")
        return []