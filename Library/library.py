from psycopg2 import connect, OperationalError
from flask import Flask, request, render_template, redirect


def take_pass():
    """
    takes password from file
    """
    with open(r"C:\\password.txt", 'r') as p:
        password = p.readline()
    return password


def select_sql(sql_code, db_name):
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


def insert_del_sql(sql_code, db_name):
    try:
        cnx = connect(user='postgres', password=take_pass(), host='localhost', database=db_name)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_code)
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
    books = select_sql(sql_query, 'library')
    return render_template("books-list.html", books=books)  # render template with context


@app.route('/add-book', methods=["GET", "POST"])
def add_book():
    """
    renders form and add taken info from form to database
    """
    if request.method == "GET":
        return render_template('add-book.html')
    elif request.method == "POST":
        title = request.form.get("title")  # takes values from inputs
        description = request.form.get("desc")
        isbn_num = request.form.get("isbn")
        if title != '' and description != '' and isbn_num != '':  # checks if user fill up the form
            sql_query = f"""INSERT INTO book(title, description, isbn_number) VALUES 
                            ('{title}', '{description}', '{isbn_num}');"""  # query for insert data
            insert_del_sql(sql_query, 'library')
            return redirect("/books-list")
        else:
            return "Form not filled properly"


@app.route('/book-details/<book_id>')
def book_details_delete_edit(book_id):
    """
    renders page with details about book taken from database
    """
    if request.method == "GET":
        sql_query = f"SELECT * FROM book WHERE id={book_id}"  # select book by id
        book = select_sql(sql_query, 'library')
        return render_template('book-details.html', book=book)
    elif request.method == "POST":
        pass

if __name__ == "__main__":
    app.run(debug=True)
