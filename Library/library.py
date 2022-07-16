from psycopg2 import connect, OperationalError
from flask import Flask, request, render_template, redirect


def take_pass():
    """
    takes password from file
    """
    with open(r"C:\\password.txt", 'r') as p:
        password = p.readline()
    return password


def execute_sql(sql_code, db_name):
    """
    Run given sql code with psycopg2

    :param sql_code: sql code to run
    :param db_name: database name
    :return: data from psycopg2 cursor as a list
    """
    try:
        cnx = connect(user='postgres', password=take_pass(), host='localhost', database=db_name)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_code)
        if cursor.rowcount > 0:
            results = []
            for row in cursor:
                results.append(row)  # add each row from database table to list
            return results
    except OperationalError as e:
        print(f"Something went wrong - {e}")
    else:
        cursor.close()
        cnx.close()


app = Flask(__name__)


@app.route("/")
def main_page():
    """
    renders main page
    """
    return render_template("main.html")


@app.route('/books-list')
def books_list():
    """
    renders template with list of books from database
    """
    sql_query = "SELECT * FROM book"
    books = execute_sql(sql_query, 'library')
    return render_template("books-list.html", books=books)  # render template with context


if __name__ == "__main__":
    app.run(debug=True)
