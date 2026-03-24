from flask import Flask, render_template, request, jsonify,g
from flask_sqlalchemy import SQLAlchemy
from HashMap import HashMap


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

total_miles = 0
packages_delivered = 0
delivery_rate = 0
packages = HashMap()
slider_value = 0


@app.route("/", methods=["POST", "GET"])
def index():
    from main import run_deliveries

    run_deliveries(slider_value)

    return render_template("dashboard.html", total_miles = total_miles, packages_delivered = packages_delivered, delivery_rate = delivery_rate)

@app.route("/packages")
def all_packages():

    from main import get_packages

    packages = get_packages()
    return render_template("all_packages.html", packages=packages)


@app.route("/slider", methods=["POST"])
def slider():

    from main import run_deliveries
    data = request.get_json()
    slider_value = float(data["value"])

    total_miles, packages_delivered, delivery_rate, addOne, addTwo, addThree, boardOne, boardTwo, boardThree, mileOne, mileTwo, mileThree  = run_deliveries(slider_value)



    return jsonify({
        "total_miles": round(total_miles, 2),
        "packages_delivered": packages_delivered,
        "delivery_rate": delivery_rate,
        "addOne": addOne,
        "addTwo": addTwo,
        "addThree": addThree,

        "boardOne": boardOne,
        "boardTwo": boardTwo,
        "boardThree": boardThree,

        "mileOne": mileOne,
        "mileTwo": mileTwo,
        "mileThree": mileThree
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




