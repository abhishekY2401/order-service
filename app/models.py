from datetime import datetime, timezone
from app.extensions import db


class Order(db.Model):
    '''
        Order Schema
    '''
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")
    items = db.relationship("OrderItem", backref="orders")

    created_at = db.Column(
        db.DateTime, default=datetime.now().astimezone(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now().astimezone(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'items': [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    '''
        Order Item Schema
    '''
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(
        db.Integer, db.ForeignKey('orders.id'), nullable=False
    )

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }
