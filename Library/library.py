from psycopg2 import connect, OperationalError
from flask import Flask, request, render_template, redirect


def take_pass():
    """
    takes password from file
    """
    with open(r"C:\\password.txt", 'r') as p:
        password = p.readline()
    return password


def insert_del_sql(sql_code, database_name):
    """
    Run given sql code with psycopg2

    :param sql_code: sql code to run
    :param database_name: database name
    :return: data from psycopg2 cursor as a list
    """
    try:
        cnx = connect(user='postgres', host='localhost', password=take_pass(),
                      database=database_name)  # open connection to database
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_code)  # execute sql code
    except OperationalError:
        print("Something went wrong")
    else:
        cursor.close()  # close cursor and connection
        cnx.close()


app = Flask(__name__)


@app.route("/")
def main_page():
    """
    renders main page
    """
    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug=True)