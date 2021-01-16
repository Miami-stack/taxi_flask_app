"""Flask-приложение такси."""
from datetime import datetime
from typing import Tuple

from flask import Flask, request, Response, jsonify
from models import Session, Drivers, Clients, Orders

app = Flask(__name__)

session = Session()


@app.route('/drivers', methods=['GET', 'POST'])
def drivers() -> Tuple[str, int]:
    """Запрос на вывод и создание водителя."""
    if request.method == 'GET':
        driver_id = request.args.get('driverId')
        driver = session.query(Drivers).filter(Drivers.id == driver_id).first()
        json_return = {"id": driver.id, "name": driver.name, "car": driver.car}
        session.close()
        return jsonify(json_return), 200

    elif request.method == 'POST':
        response_post = request.json
        name = response_post['name']
        car = response_post['car']
        create_driver = Drivers(name=name, car=car)
        session.add(create_driver)
        print(create_driver.__repr__())
        session.commit()
        session.close()
        return 'created!', 200
    assert False


@app.route('/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id: int) -> Tuple[str, int]:
    """Запрос удаления водителя."""
    deleted_driver = session.query(Drivers).filter_by(id == driver_id).first()
    session.delete(deleted_driver)
    print(f"Из базы удалился водитель {deleted_driver}")
    session.commit()
    session.close()
    return 'Удалено', 204


@app.route('/clients', methods=['POST', 'GET'])
def clients() -> Tuple[str, int]:
    """Запрос на вывод и создание клиента."""
    if request.method == 'GET':
        client_id = request.args.get('clientId')
        client = session.query(Clients).filter(Clients.id == client_id).first()
        json_return = {'id': client.id, 'name': client.name,
                       'is_vip': client.is_vip}
        return jsonify(json_return)

    elif request.method == 'POST':
        response_post = request.json
        name = response_post['name']
        is_vip = response_post['is_vip']
        create_client = Clients(name, is_vip)
        session.add(create_client)
        print(create_client.__repr__())
        session.commit()
        session.close()
        return 'created!', 200
    assert False


@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id: int) -> Response:
    """Метод по удалению клиента."""
    deleted_client = session.query(Clients).filter_by(id == client_id).first()
    session.delete(deleted_client)
    print(f"Из базы удалился клиент {deleted_client}")
    session.commit()
    session.close()
    return Response('Удалено', status=204)


@app.route('/orders', methods=['POST', 'GET'])
def post_order() -> Tuple[str, int]:
    """Запрос на вывод и создание заказа."""
    if request.method == 'GET':
        order_id = request.args.get('orderId')
        order = session.query(Orders).filter(Orders.id == order_id).first()
        json_return = {'id': order.id, 'address_from': order.address_from,
                       'address_to': order.address_to,
                       'client_id': order.client_id,
                       'driver_id': order.driver_id,
                       'date_created': order.date_created,
                       'status': order.status}
        return jsonify(json_return)

    if request.method == 'POST':
        response_post = request.json
        address_from = response_post['address_from']
        address_to = response_post['address_to']
        client_id = response_post['client_id']
        driver_id = response_post['driver_id']
        date_created = datetime.now()
        status = response_post['status']
        posted_order = Orders(address_from, address_to,
                              client_id, driver_id, date_created, status)
        session.add(posted_order)
        session.commit()
        session.close()
        return '', 200
    assert False


@app.route('/orders/<int:order_id>', methods=['PUT'])
def put_order(order_id: int) -> Tuple[str, int]:
    """Метод по апдейту заказа."""
    order = session.query(Orders).filter(Orders.id == order_id).first()
    response_post = request.json

    if order.status == 'not_accepted' and response_post['status'] == 'in progress' or \
            response_post['status'] == 'cancelled':
        status = response_post['status']

        session.query(Orders).filter(Orders.id == order_id).update({Orders.status: status,
                                                                    Orders.date_created: datetime.now()})
        session.commit()
        session.close()
        return 'Изменено!', 200

    if order.status == 'in progress' and response_post['status'] == 'done' or \
            response_post['status'] == 'cancelled':
        status = response_post['status']
        session.query(Orders).filter(Orders.id == order_id).update({Orders.status: status,
                                                                    Orders.date_created: datetime.now()})
        session.commit()
        session.close()
        return 'Изменено!', 200
    assert False


app.run(host="127.0.0.1", port=5050, debug=True)
