from conexion.conexionBD import connectionBD  # Conexión a BD
import pdb;

def procesar_form_grupo(grado, id_docente):

    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:

                    sql = "INSERT INTO grupo (grado, id_docente) VALUES (%s, %s)"
                    valores = (grado, id_docente)
                    mycursor.execute(sql, valores)
                    conexion_MySQLdb.commit()
                    resultado_insert = mycursor.rowcount
                    return resultado_insert
    except Exception as e:
            print(f"Error en el Insert Grupo: {e}")
            return []
    
def sql_lista_docentes():
    try:
        with connectionBD() as conexion_MySQLdb:
            
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT id_docente, CONCAT(nombres,' ',apellidos) AS Full_Name FROM docente"
                  
                cursor.execute(querySQL,)
                listaDocentes = cursor.fetchall()
        return listaDocentes
    except Exception as e:
        print(
            f"Error en la función sql_lista_docentes: {e}")
        return None
    
    # Lista de Grupos
def sql_lista_grupo():
    try:
        with connectionBD() as conexion_MySQLdb:
            
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT g.id_grupo, g.grado, g.id_docente, CONCAT(d.nombres , ' ' , d.apellidos) as nombres_docente FROM grupo g inner join docente d on d.id_docente = g.id_docente"
                  
                cursor.execute(querySQL,)
                grupos = cursor.fetchall()
        return grupos
    except Exception as e:
        print(
            f"Errro en la función sql_lista_grupo: {e}")
        return None
    
    # Eliminar grupo
def eliminarGrupo(id_grupo):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM grupo WHERE id_grupo=%s"
                cursor.execute(querySQL, (id_grupo,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarGrupo : {e}")
        return []
