#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask, flash, render_template, request, url_for, redirect, make_response
from flask.ext import excel
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'some_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)


class Funcionario(db.Model):
	__tablename__ = 'funcionario'
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nome = db.Column(db.String)
	email = db.Column(db.String)
	telefone = db.Column(db.String)
	salmensal = db.Column(db.Float)
	media = db.Column(db.Float)
	receita = db.Column(db.Float)
	bonus = db.Column(db.Float)
	

	def __init__(self, nome, email, telefone, salmensal, media, receita, bonus):
		self.nome = nome
		self.email = email
		self.telefone = telefone
		self.salmensal = salmensal
		self.media = media
		self.receita = receita
		self.bonus = bonus
		
db.create_all()




@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/")
@app.route("/cadastrar")
def cadastrar():
	return render_template("cadastro.html")

def voltar():
	return render_template("home")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
	if request.method == "POST":
		nome = (request.form.get("nome"))
		email = (request.form.get("email"))
		telefone = (request.form.get("telefone"))
		salmensal = (request.form.get("salmensal"))
		#media = (request.form.get("media"))
		#receita = (request.form.get("receita"))
		bonus = (request.form.get("bonus"))
		

		if nome and email and telefone and salmensal and bonus:
			receita = 12 * float(salmensal) + float(bonus)
			media = (receita / 12)
			p = Funcionario(nome, email, telefone, salmensal, "%.2f" % media, receita, bonus)
			db.session.add(p)
			db.session.commit()
			flash("Cadastrado com sucesso!!!")			
			
	return redirect(url_for("home"))

@app.route("/lista")
def lista():
	funcionario = Funcionario.query.all()
	return render_template("lista.html", funcionario=funcionario)



@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
	funcionario = Funcionario.query.filter_by(_id=id).first()
	nome = get(funcionario.nome)
	if request.method == "POST":
		nome = (request.form.get("nome"))
		email = (request.form.get("email"))
		telefone = (request.form.get("telefone"))
		salmensal = (request.form.get("salmensal"))
		bonus = (request.form.get("bonus"))

		if nome and email and telefone and salmensal and bonus:
			funcionario.nome = nome
			funcionario.email = email
			funcionario.telefone = telefone
			funcionario.salmensal = salmensal
			funcionario.bonus = bonus
			db.session.commit()

	return render_template("atualizar.html", funcionario=funcionario)

@app.route("/excluir/<int:id>")
def excluir(id):
	funcionario = Funcionario.query.filter_by(_id=id).first()

	db.session.delete(funcionario)
	db.session.commit()
	
	funcionario = Funcionario.query.all()
	return render_template("lista.html", funcionario=funcionario)

@app.route('/download', methods=['GET'])
def download():
	query_sets = Funcionario.query.all()
    	column_names = ['_id', 'nome', 'email', 'telefone', 'salmensal', 'bonus']
    	return excel.make_response_from_query_sets(query_sets, column_names, "csv")


if __name__ == "__main__":
	app.run(debug=True)
