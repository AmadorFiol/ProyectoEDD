from crypt import methods

from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_estudiante = db.Column(db.String(100), nullable=False)
    materia=db.column(db.String(100),nullable=False)
    nota=db.column(db.Integer, nullable=False)
    fecha_registro=db.column(db.String(100),nullable=False)

    def __repr__(self):
        return f'estudiante {self.nombre_estudiante}'

@app.route('/estudiantes')
def get_estudiantes():
    estudiantes = Estudiante.query.all()
    return render_template("estudiantes.html", estudiantes=estudiantes)


@app.route('/add_estudiante', methods=['POST','GET'])
def add_estudiante():
    if request.method =='POST':
        nombre = request.form.get("nombre_estudiante")
        materia = request.form.get("materia")
        nota=request.form.get("nota")
        fecha_registro=request.form.get("fecha_registro")
        usuario_nuevo = Estudiante(nombre_estudiante= nombre, materia= materia,nota= nota,fecha_registro= fecha_registro)
        db.session.add(usuario_nuevo)
        db.session.commit()
        return redirect(url_for('get_estudiantes'))
    else:
        return render_template('agregar.html')

@app.route('/estudiantes/<int:estudiante_id>')
def get_estudiante_by_id(estudiante_id):
    estudiante = Estudiante.query.get(estudiante_id)
    if estudiante:
        return jsonify({"id": estudiante.id, "nombre_estudiante": estudiante.nombre_estudiante, "materia": estudiante.materia, "nota":estudiante.nota,"fecha_registro":estudiante.fecha_registro})
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/estudiante/delete/<int:estudiante_id>', methods=['POST'])
def delete_estudiante(estudiante_id):
    estudiante= Estudiante.query.get(estudiante_id)
    if estudiante:
        db.session.delete(estudiante)
        db.session.commit()
        return redirect(url_for('get_estudiantes'))

    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/estudiante/edit_estudiante/<int:estudiante_id>', methods=['GET', 'POST'])
def edit_estudiante(estudiante_id):
    estudiante = Estudiante.query.get(estudiante_id)
    if not estudiante:
        return "Estudiante no encontrado", 404
    if request.method == 'POST':
        estudiante.nombre_estudiante = request.form.get('nombre_estudiante')
        estudiante.materia = request.form.get('materia')
        db.session.commit()
        return redirect(url_for('get_estudiantes'))

    return render_template('edit_estudiante.html', estudiante=estudiante)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)