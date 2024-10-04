from ariadne import MutationType, QueryType
from app.models import Order, OrderItem, OrderUser, ProductCatalog
from app.rabbitmq import publish_event
from app.utils import fetch_product_prices
from app.extensions import db
from config import Config
import logging
import json

query = QueryType()
mutation = MutationType()


@query.field("allOrders")
def fetch_all_orders(*_):
    try:
        orders = Order.query.all()
        return orders
    except Exception as e:
        logging.error(f"Error fetching products: {e}")
        return []


def fetch_order(_, info, id):
    try:
        # product_id = info.context.get("product_id")
        order = Order.query.get(id)
        if not order:
            raise Exception(f"Product with id {id} not found")
        return order
    except Exception as e:
        logging.error(f"Error fetching order: {e}")
        return None

# handle creation of order


@mutation.field("createOrder")
def handle_create_order(_, info, user_id, order_items):
    try:

        # Check if all the products are in stock
        for item in order_items:
            product_id = item['product_id']
            order_quantity = item['quantity']

            product = ProductCatalog.query.filter_by(
                product_id=product_id).first()

            if product is None:
                logging.error(f"Product with ID {product_id} does not exist.")
                return {
                    "success": False,
                    "errors": [f"Product with ID {product_id} not found."]
                }

            if product.quantity < order_quantity:
                logging.error(
                    f"Requested quantity of product ID {product_id} not present in stock. "
                    f"Available: {product.quantity}, Requested: {order_quantity}")
                return {
                    "success": False,
                    "errors": [f"Requested quantity of product ID {product_id} not available."]
                }

        # Grouping all the product ids to make a single request and fetch all the prices
        product_ids = [item['product_id'] for item in order_items]

        logging.info(f"extract all product ids: {product_ids}")

        # Fetch product prices from the Product Microservice
        product_prices = fetch_product_prices(product_ids)
        logging.info(f"get all product prices: {product_prices}")

        # Calculate total amount using fetched product prices
        total_amount = 0
        order_item_objects = []

        for item in order_items:
            product_id = str(item['product_id'])
            quantity = item['quantity']

            # Check if the product exists
            if product_id not in product_prices:
                logging.info("product does not exist in product_prices")
                return {
                    "success": False,
                    "errors": [f"Product with ID {product_id} not found."]
                }

            total_amount += product_prices[product_id] * quantity
            logging.info(
                f"determine the total amount for the order: {total_amount}")

        user = OrderUser.query.filter_by(user_id=user_id).first()
        address = user.address

        # Create the new order
        new_order = Order(
            user_id=user_id, total_amount=total_amount, address=address)

        for item in order_items:
            product_id = item['product_id']
            quantity = item['quantity']

            # Create order items
            order_item = OrderItem(product_id=product_id, quantity=quantity)
            db.session.add(order_item)

            order_item_objects.append(order_item)
            logging.info(f"created an order item for product id: {product_id}")

        # Add the order items to the order
        new_order.items = order_item_objects

        # Add the new order and commit both order and order items
        db.session.add(new_order)
        db.session.commit()

        # Emit "Order Placed" event
        event_data = json.dumps({
            'order_id': new_order.id,
            'user_id': new_order.user_id,
            'total_amount': new_order.total_amount,
            'items': [item.to_dict() for item in new_order.items]
        })

        publish_event(exchange_name="event_exchange",
                      routing_key=Config.ORDER_PLACED_QUEUE, message=event_data)
        logging.info(f"emit event to queue: {event_data}")

        return {
            "success": True,
            "order": new_order.to_dict()
        }

    except Exception as error:
        db.session.rollback()
        logging.error(f"Error creating order: {str(error)}")
        return {
            "success": False,
            "errors": [str(error)],
        }


# @mutation.field("updateOrderStatus")
# def func():
#     pass
