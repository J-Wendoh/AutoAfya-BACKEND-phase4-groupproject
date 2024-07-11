from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
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

    # Relationship mapping the booking to related bookingservice
    bookingservices = db.relationship('BookingService', back_populates='booking', cascade='all, delete-orphan')

    # Association proxy to get services for this booking through bookingservice
    services = association_proxy('bookingservices', 'service', creator=lambda service_obj: BookingService(service=service_obj))

    def __repr__(self):
        return f'<Booking {self.id}| {self.booking_date} | {self.total_cost}>'

class Service(db.Model, SerializerMixin):
    __tablename__ = 'services'

    serialize_rules = ('-reviews', '-bookings', '-bookingservices')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80))
    service_image = db.Column(db.String)
    cost = db.Column(db.Float, nullable=False)

    reviews = db.relationship('Review', back_populates='service')

    # Relationship mapping the service to related bookingservice
    bookingservices = db.relationship('BookingService', back_populates='service', cascade='all, delete-orphan')

    # Association proxy to get bookings for this service through bookingservice
    bookings = association_proxy('bookingservices', 'booking', creator=lambda booking_obj: BookingService(booking=booking_obj))

    def __repr__(self):
        return f'<Service {self.name} | {self.cost}>'

class BookingService(db.Model, SerializerMixin):
    __tablename__ = 'bookingservices'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship mapping the bookingservice to related booking
    booking = db.relationship('Booking', back_populates='bookingservices')
    # Relationship mapping the bookingservice to related service
    service = db.relationship('Service', back_populates='bookingservices')

    def __repr__(self):
        return f'<Booking Service {self.id} | {self.service.name} | {self.booking.booking_date}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Check constraint to limit rating to values between 1 and 5
    __table_args__ = (
        db.CheckConstraint('rating >= 1'),
        db.CheckConstraint('rating <= 5')
    )

    user = db.relationship('User', back_populates='reviews')
    service = db.relationship('Service', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.content}>'
