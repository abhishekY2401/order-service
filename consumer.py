from app.models import OrderUser, ProductCatalog, db
from app.rabbitmq import consume_events
from main import app
import json
import logging


def create_user_in_orders(user_data):
    try:
        with app.app_context():
            user_id = user_data['user_id']
            email = user_data['email']
            address = user_data['address']
            contact = user_data['contact']

            # Check if the user already exists in the OrderUser model
            existing_user = OrderUser.query.filter_by(user_id=user_id).first()

            if not existing_user:
                # Create a new OrderUser entry
                new_order_user = OrderUser(
                    user_id=user_id,
                    email=email,
                    contact=contact,
                    address=address
                )
                db.session.add(new_order_user)
                db.session.commit()
                logging.info(f"Created new OrderUser for user_id {user_id}")
            else:
                logging.info(f"OrderUser already exists for user_id {user_id}")

    except Exception as error:
        logging.error(f"Exception while creating a user in order: {error}")


def update_user_in_orders(user_data):
    try:
        with app.app_context():
            user_id = user_data['user_id']
            email = user_data['email']
            new_address = user_data['address']
            new_contact = user_data['contact']

            # Fetch the OrderUser entry based on the user_id
            order_user = OrderUser.query.filter_by(user_id=user_id).first()

            if order_user:
                # Update the user details
                order_user.email = email
                order_user.address = new_address
                order_user.contact = new_contact
                db.session.commit()
                print(f"Updated user details for user_id {user_id}")
            else:
                print(f"No OrderUser found for user_id {user_id}")

    except Exception as error:
        logging.error(f"Error while updating user: {error}")


def create_product_in_order(product_data):
    try:
        with app.app_context():
            product_id = product_data['id']
            product_name = product_data['name']
            product_price = product_data['price']
            product_quantity = product_data['quantity']

            # Insert new product entry if it doesn't exist
            new_product = ProductCatalog(
                product_id=product_id,
                name=product_name,
                price=product_price,
                quantity=product_quantity
            )
            db.session.add(new_product)
            logging.info(
                f"Added new product to ProductCatalog: {product_name}")

            # Commit changes
            db.session.commit()

    except Exception as error:
        logging.error(f"Error while creating or updating product: {error}")


def update_inventory_in_order(product_data):
    try:
        with app.app_context():

            products = product_data

            for item in products:
                product_id = item['product_id']
                product_quantity = item['quantity']

                # Check if the product already exists in the ProductCatalog
                product_catalog_entry = ProductCatalog.query.filter_by(
                    product_id=product_id).first()

                if product_catalog_entry:
                    product_catalog_entry.quantity = product_quantity

                    logging.info(
                        f"Updated ProductCatalog for product_id {product_id}")

            # Commit changes
            db.session.commit()

    except Exception as error:
        logging.error(f"Error while updating product: {error}")


def on_message_received(ch, method, properties, body):
    logging.info(f"Received event: {body}")

    event_data = json.loads(body)
    event_type = method.routing_key

    if event_type == 'user.registered':
        create_user_in_orders(event_data)
    elif event_type == 'user.profile.updated':
        update_user_in_orders(event_data)
    elif event_type == 'product.created':
        create_product_in_order(event_data)
    elif event_type == 'inventory.updated':
        update_inventory_in_order(event_data)
    else:
        print(f"Unhandled event type: {event_type}")


if __name__ == '__main__':
    consume_events(on_message_received)
