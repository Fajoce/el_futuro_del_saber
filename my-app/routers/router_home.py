from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error
from conexion import conexionBD
import pdb

# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/estudiantes"


@app.route('/registrar-estudiante', methods=['GET'])
def viewFormEstudiante():
    if 'conectado' in session:
        print('Listo')
        return render_template(f'{PATH_URL}/form_estudiante.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-estudiante', methods=['POST'])
def formEstudiante():
    if 'conectado' in session:   
                if request.method == 'POST' and 'tipo_doc' in request.form and 'num_doc' in request.form  and 'nombres' in request.form and 'apellidos' in request.form and 'fecha_nacimiento' in request.form and 'grado' in request.form and 'direccion' in request.form and 'email' in request.form and 'tel_fijo' in request.form:
                    tipo_doc = request.form['tipo_doc']
                    num_doc = request.form['num_doc']
                    nombres = request.form['nombres']
                    apellidos = request.form['apellidos']
                    fecha_nacimiento = request.form['fecha_nacimiento']
                    grado = request.form['grado']
                    direccion = request.form['direccion']
                    email = request.form['email']
                    tel_fijo = request.form['tel_fijo']

                    resultado = procesar_form_estudiante(tipo_doc, num_doc, nombres, apellidos,fecha_nacimiento, grado, direccion, email, tel_fijo)
                    if resultado:
                     return redirect(url_for('lista_estudiantes'))  
                    else:
                     flash('primero debes iniciar sesión.', 'error')
                     return redirect(url_for('inicio'))


@app.route('/lista-de-estudiantes', methods=['GET'])
def lista_estudiantes():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_estudiantes.html', estudiantes=sql_lista_estudiantesBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-estudiante/", methods=['GET'])
@app.route("/detalles-estudiante/<int:id_estudiante>", methods=['GET'])
def detalleEstudiante(id_estudiante=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEstudiante es None o no está presente en la URL
        if id_estudiante is None:
            return redirect(url_for('inicio'))
        else:
            detalle_estudiante = sql_detalles_estudiantesBD(id_estudiante) or []
            return render_template(f'{PATH_URL}/detalles_estudiante.html', detalle_estudiante=detalle_estudiante)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscador de estudiantes
@app.route("/buscando-estudiante", methods=['POST'])
def viewBuscarEstudianteBD():
    resultadoBusqueda = buscarEstudianteBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_estudiante.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route('/editar-estudiante/<string:id_estudiante>', methods=['GET'])
def viewEditarEstudiante(id_estudiante):
    if 'conectado' in session:
        respuestaEstudiante = buscarEstudianteById(id_estudiante)
        if respuestaEstudiante:
            return render_template(f'{PATH_URL}/form_estudiante_update.html', respuestaEstudiante=respuestaEstudiante)
        else:
            flash('El estudiante no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion del estudiante
@app.route('/actualizar-estudiante', methods=['POST'])
def actualizarEstudiante():
    try: 
        resultData = procesar_actualizacion_form(request)
        if resultData:
            flash('Estudiante actualizado correctamente.', 'success')
        else:
            flash('No se pudo actualizar el estudiante.', 'error')
        return redirect(url_for('lista_estudiantes'))
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash('Error inesperado al actualizar estudiante.', 'error')
        return redirect(url_for('lista_estudiantes'))


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))


@app.route('/borrar-estudiante/<string:id_estudiante>', methods=['GET'])
def borrarEstudiante(id_estudiante):
    resp = RemoverEstudiante(id_estudiante)
    if resp:
        flash('El Estudiante fue eliminado correctamente', 'success')
        return redirect(url_for('lista_estudiantes'))


@app.route("/descargar-informe-estudiante", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/lista-estudiantes')
def paginador_lista_estudiantes():
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    pagina = request.args.get('pagina', default=1, type=int)
    por_pagina = 10
    offset = (pagina - 1) * por_pagina

    estudiantes = obtener_estudiantes_paginados(offset=offset, limit=por_pagina)
    total_estudiantes = contar_estudiantes()
    total_paginas = (total_estudiantes + por_pagina - 1) // por_pagina

    return render_template(
        f'{PATH_URL}/lista_estudiantes.html',
        estudiantes=estudiantes,
        pagina=pagina,
        total_paginas=total_paginas
    )
