# from sqlalchemy.orm import validates
# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable = False)
    image_url = db.Column(db.String)
    bookings = db.relationship('Booking', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')


    def __repr__(self):
        return f'<User {self.username}>'

class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    total_cost = db.Column(db.Float, nullable=False, default=0.0)

    user = db.relationship('User', back_populates='bookings')
    services = db.relationship('BookingService', back_populates='booking')

    def __repr__(self):
        return f'<Booking {self.total_cost}>'

class Service(db.Model, SerializerMixin):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80))
    cost = db.Column(db.Float, nullable=False)

    reviews = db.relationship('Review', back_populates='service')

    def __repr__(self):
        return f'<Service {self.name}>'

class BookingService(db.Model, SerializerMixin):
    __tablename__ = 'bookingservices'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    booking = db.relationship('Booking', back_populates='services')
    service = db.relationship('Service')

    def __repr__(self):
        return f'<Service {self.name}>'

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='reviews')
    service = db.relationship('Service', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.content}>'
