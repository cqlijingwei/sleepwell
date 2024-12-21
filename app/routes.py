from flask import Blueprint, request, jsonify
from app.utils.context_router import ContextRouter
from app.agents.product_details import ProductDetailsAgent
from app.agents.product_reviews import ProductReviewsAgent
from app.agents.orders import OrdersAgent
import yaml

api = Blueprint('api', __name__)


# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize agents
product_details_agent = ProductDetailsAgent(config)
product_reviews_agent = ProductReviewsAgent(config)
orders_agent = OrdersAgent(config)

# Initialize router
router = ContextRouter({
    'product_details': product_details_agent,
    'product_reviews': product_reviews_agent,
    'orders': orders_agent
})

@api.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')
    context = data.get('context')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    response = router.route_query(query, context)
    return jsonify({'response': response})

@api.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order_id = orders_agent.create_order(
        data['customer_email'],
        data['product_name'],
        data['size'],
        data['price'],
        data['shipping_address']
    )
    return jsonify({'order_id': order_id})

@api.route('/orders/<order_id>', methods=['GET'])
def get_order_status(order_id):
    status = orders_agent.get_order_status(order_id)
    return jsonify(status)

@api.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    result = product_reviews_agent.add_review(
        data['customer_email'],
        data['product_name'],
        data['rating'],
        data['comment']
    )
    return jsonify({'message': result})