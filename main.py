from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from forms import ToDoForm
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.secret_key = os.environ.get("key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///todo.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


##CONFIGURE TABLES
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    todos = db.Column(db.String, nullable=True)


db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    form = ToDoForm()
    if form.validate_on_submit():
        name_list = [data.name for data in db.session.query(Todo).all()]
        if form.name.data not in name_list:
            todostring = form.text.data + "%&$"
            new_todo = Todo(name=form.name.data, todos=todostring)
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for("todo_page", pname=form.name.data))
        else:
            flash("Your name is not available")
            return redirect(url_for("home"))
    return render_template("index.html", form=form, Is_log=False)


@app.route("/<pname>", methods=["GET", "POST"])
def todo_page(pname):
    todos_obj = Todo.query.filter_by(name=pname).first()
    form = ToDoForm(name=pname)
    todo_string = todos_obj.todos
    todo_string_list = todo_string.split("%&$")
    checked = [todo_string_list[int(index)] for index in request.args.getlist("check")]


    if form.validate_on_submit():
        checked = [todo_string_list[int(index)] for index in request.form.getlist("check")]
        todos_obj = Todo.query.filter_by(name=pname).first()
        todos_obj.todos = todo_string + form.text.data + "%&$"
        todo_string_list.append(form.text.data)
        db.session.commit()


    return render_template("index.html", form=form, list=todo_string_list, Is_log=True, checked_list=checked)


if __name__ == "__main__":
    app.run(debug=True)
