from crypt import methods

from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'User {self.name}'

@app.route('/users')
def get_users():
    users = User.query.all()
    #return jsonify([{"id" : user.id, "name": user.name, "email": user.email} for user in users])
    return render_template("users.html", users=users)


@app.route('/add_user', methods=['POST','GET'])
def add_user():
    if request.method =='POST':
        nombre = request.form.get("name")
        email = request.form.get("email")
        usuario_nuevo = User(name= nombre, email= email)
        db.session.add(usuario_nuevo)
        db.session.commit()
        return redirect(url_for('get_users'))
    else:
        return render_template('agregar.html')

@app.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email})
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user= User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('get_users'))

    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/user/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return "Usuario no encontrado", 404
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        db.session.commit()
        return redirect(url_for('get_users'))

    return render_template('edit_user.html', user=user)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)