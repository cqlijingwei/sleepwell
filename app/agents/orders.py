from app.agents.base import BaseAgent
from app.models import Order
from datetime import datetime, timedelta
import random
import string

class OrdersAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
    
    def process_query(self, query, context=None):
        if not self.is_enabled:
            return self.format_response(None)
            
        # Process order-related queries
        # Implementation would include creating orders and checking order status
        pass
    
    def create_order(self, customer_email, product_name, size, price, shipping_address):
        order_id = 'UC' + ''.join(random.choices(string.digits, k=6))
        delivery_date = datetime.utcnow() + timedelta(days=7)
        
        order = Order(
            id=order_id,
            customer_email=customer_email,
            product_name=product_name,
            size=size,
            price=price,
            status='processing',
            delivery_date=delivery_date,
            shipping_address=shipping_address
        )
        
        db.session.add(order)
        db.session.commit()
        
        return order_id
    
    def get_order_status(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return "Order not found"
        return {
            'status': order.status,
            'delivery_date': order.delivery_date,
            'product_name': order.product_name
        }