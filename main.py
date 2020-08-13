# The main module, where the application starts

from logic.logic import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database = SQLAlchemy(app)

class user(database.Model):
    _id = database.Column("id", database.Integer, primary_key = True)
    name = database.Column(database.String(100))
    score = database.Column(database.Integer)
    date = database.Column(database.String(100))

    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

logic = logic()

#database.session.query(user).delete()
#database.session.commit()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        logic.prepare_game()
        return render_template("index.html", row = [1, 2, 3, 4, 5, 6, 7, 8], column = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], highscores = sorted(user.query.all(), key = lambda x: (x.score, x.date))[0:50])

    elif request.method == "POST":
        if "name" in request.form:
            if logc.get_steps >= 9:
                database.session.add(user(request.form["name"], logic.get_steps))
                database.session.commit()
            return redirect(url_for("home"))

        elif "over" in request.form:
            return logic.get_remaining_squares()

        row = request.form["row"]
        column = request.form["column"]

        if len(logic.get_number_of_battleships_placed) != 3:
            return logic.place_battleships(row, column)
        else:
            return logic.advance_game(int(row), int(column))
    else:
        return redirect(url_for("home"))

if __name__=='__main__':
    database.create_all()
    app.run(debug=True)
    