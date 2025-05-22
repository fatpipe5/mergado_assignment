from flask import Flask, request, jsonify, abort
from db import db
from models import Order
from schemas import OrderCreate, OrderOut
from currency_rates import ALLOWED_CURRENCIES, get_rates, convert_price
from pydantic import ValidationError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

def row_to_schema(order, target=None, rates=None):
    """Konvertuje riadok z DB na OrderOut dictionary"""
    price = order.price
    currency = order.currency
    if target:
        price = convert_price(order.price, order.currency, target, rates)
        currency = target
    return OrderOut(
        id=order.id,
        customer_name=order.customer_name,
        price=price,
        currency=currency,
    ).model_dump()

#---------- endpointy ----------
@app.post("/orders")
def create_order():
    if not request.is_json:
        abort(400, "Request must be JSON.")
    data = request.get_json()

    #Pydantic validacia
    try:
        order_in = OrderCreate.model_validate(data)
    except ValidationError as err:
        return jsonify(err.errors()), 400

    #ulozenie do DB
    order = Order(
        customer_name=order_in.customer_name,
        price=order_in.price,
        currency=order_in.currency,
    )
    db.session.add(order)
    db.session.commit()

    return jsonify(row_to_schema(order)), 201


@app.get("/orders")
def list_orders():
    target = request.args.get("to_currency", "").upper() or None
    if target and target not in ALLOWED_CURRENCIES:
        abort(400, "Unsupported to_currency.")

    if target:
        rates = get_rates()
    else:
        rates = None

    orders = Order.query.all()

    #zmena kazdeho riadku v DB na dictionary
    response_payload = []
    for order in orders:
        order_dict = row_to_schema(order, target, rates)
        response_payload.append(order_dict)

    return jsonify(response_payload)



@app.get("/orders/<int:oid>")
def get_order(oid):
    target = request.args.get("to_currency", "").upper() or None
    if target and target not in ALLOWED_CURRENCIES:
        abort(400, "Unsupported to_currency.")

    if target:
        rates = get_rates()
    else:
        rates = None

    order = Order.query.get_or_404(oid)
    order_dict = row_to_schema(order, target, rates)
    return jsonify(order_dict)


@app.delete("/orders/<int:oid>")
def delete_order(oid):
    order = Order.query.get_or_404(oid)

    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": f"Order with id {oid} successfully deleted"}), 200



if __name__ == "__main__":
    app.run(debug=True)
