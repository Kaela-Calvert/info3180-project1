from app import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    bedrooms = db.Column(db.String(10), nullable=False)
    bathrooms = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(100), nullable=False)  # Assuming the filename is stored
    
    def __init__(self, title, bedrooms, bathrooms, location, price, type, description, photo):
        self.title = title
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.location = location
        self.price = price
        self.type = type
        self.description = description
        self.photo = photo
    
    def __repr__(self):
        return f"Property('{self.title}', '{self.location}', '{self.price}')"
