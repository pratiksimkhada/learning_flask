from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

def connect_database():
	conn = sqlite3.connect("sqlite.db")
	conn.row_factory = sqlite3.Row
	return conn

@app.route("/")
def home():
	conn = connect_database()

	rows = conn.execute("SELECT * FROM movies").fetchall()
	conn.close()

	return render_template('home.html', rows=rows)


@app.route("/add-movies", methods = ['POST', 'GET'])
def add_movies():
	if request.method=='POST':
		title = request.form['title']
		genre = request.form['genre']
		year = request.form['year']

		with sqlite3.connect("sqlite.db") as con:
			cur = con.cursor()
			cur.execute("INSERT into movies(title, genre, released_year) VALUES (?,?,?)", (title, genre, year) )

			con.commit()
			return redirect(url_for('home'))


	return render_template('add_movies.html')


@app.route("/edit-movie/<movie_id>", methods=["POST", "GET"])
def edit_movies(movie_id):
	id=movie_id

	conn = connect_database()
	movie = conn.execute("SELECT * FROM movies WHERE movie_id=?", (id)).fetchone()

	if request.method== "POST":
		title = request.form['title']
		genre = request.form['genre']
		year = request.form['year']

		conn.execute(" UPDATE movies SET title=?, genre=?, released_year=? WHERE movie_id=? ", (title, genre, year, id))		
		conn.commit()
		
		return redirect(url_for('home'))

	conn.close()
	
	return render_template('edit_movie.html', movie=movie)

@app.route("/delete-movie/<movie_id>")
def delete_movie(movie_id):
	id=movie_id

	conn = connect_database()
	conn.execute("DELETE FROM movies WHERE movie_id=?", (id))
	conn.commit()
	conn.close()
	return redirect(url_for('home'))