from flask import Flask, request
from flasgger import Swagger, swag_from
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)

# Microservice configs
CONFIG = {'AMQP_URI': "amqp://guest:guest@rabbitmq"}


@app.route('/order', methods=['POST'])
@swag_from('order.yml')
def order():
    order_details = request.json.get('order')
    email = request.json.get('email')
    mobile = request.json.get('mobile')
    msg = (
        f"The order for {order_details} was placed successfully,"
        f"you'll receive an email confirmation soon."
    )
    with ClusterRpcProxy(CONFIG) as rpc:
        rpc.order_processing_service.process.call_async(order_details, email, mobile)
        return msg, 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
