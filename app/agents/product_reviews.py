from app.agents.base import BaseAgent
from app.models import Review, Order
import json

class ProductReviewsAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.reviews = self._load_reviews()
    
    def _load_reviews(self):
        with open('data/product_reviews.json', 'r') as f:
            return json.load(f)
    
    def process_query(self, query, context=None):
        if not self.is_enabled:
            return self.format_response(None)
            
        # Process review-related queries
        # Implementation would include handling review requests and adding new reviews
        pass
    
    def add_review(self, customer_email, product_name, rating, comment):
        # Verify purchase
        order = Order.query.filter_by(
            customer_email=customer_email,
            product_name=product_name
        ).first()
        
        if not order:
            return "You can only review products you have purchased."
        
        review = Review(
            product_name=product_name,
            rating=rating,
            comment=comment,
            customer_email=customer_email,
            verified_purchase=True
        )
        
        db.session.add(review)
        db.session.commit()
        
        return "Thank you for your review!"