from flask import Blueprint, request, session, make_response, jsonify
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from models import db, Booking, Service, BookingService, User
from flask_restful import Api, Resource, reqparse
from datetime import datetime
# from auth import allow
customer_bp = Blueprint('customer_bp',__name__, url_prefix='/customer')


customer_api = Api(customer_bp)

booking_args = reqparse.RequestParser()


class ServiceResource(Resource):

    @jwt_required()
    def get(self):
        services = [service.to_dict() for service in Service.query.all()]
        # return make_response(jsonify(services), 200)
        return services

customer_api.add_resource(ServiceResource, '/services')


class BookingById(Resource):

    @jwt_required()
    def post(self):
        # Define request parser and expected arguments
        parser = reqparse.RequestParser()
        parser.add_argument('booking_date', required=True, help='Booking date cannot be blank', type=str)
        parser.add_argument('service_ids', required=True, help='Service IDs cannot be blank', type=list, location='json')
        args = parser.parse_args()

        # Get current user ID from JWT token
        user_id = get_jwt_identity()

        # Parse booking date
        try:
            booking_date = datetime.strptime(args['booking_date'], '%d/%m/%Y').date()
        except ValueError:
            return {'message': 'Invalid date format. Use DD/MM/YY.'}, 400

        # Get services and calculate total cost
        service_ids = args['service_ids']
        services = Service.query.filter(Service.id.in_(service_ids)).all()
        if not services:
            return {'message': 'No valid services found.'}, 400

        total_cost = sum(service.cost for service in services)

        # Create new booking
        booking = Booking(user_id=user_id, booking_date=booking_date, total_cost=total_cost)
        db.session.add(booking)
        db.session.commit()

        # Create BookingService entries
        for service in services:
            booking_service = BookingService(booking_id=booking.id, service_id=service.id)
            db.session.add(booking_service)

        db.session.commit()

        return make_response(jsonify({'message': 'Booking created successfully', 'booking_id': booking.id, 'total_cost': total_cost}), 201)


    @jwt_required()
    def get(self):
        # Get current user ID from JWT token
        user_id = get_jwt_identity()

        # Query bookings for the current user
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        # Fetch bookings and their total costs
        bookings = Booking.query.filter_by(user_id=user_id).all()
        bookings_data = [
            {
                'booking_id': booking.id,
                'booking_date': booking.booking_date.strftime('%d/%m/%Y'),
                'total_cost': booking.total_cost,
                'services': [
                    {
                        'service_id': service.id,
                        'service_name': service.name,
                        'service_cost': service.cost
                    } for service in booking.services
                ]
            }
            for booking in bookings
        ]

        return jsonify(bookings_data)

customer_api.add_resource(BookingById, '/booking')



class UpdateBooking(Resource):

    @jwt_required()
    def patch(self, booking_id):
        # Define request parser and expected arguments
        parser = reqparse.RequestParser()
        parser.add_argument('booking_date', required=False, type=str)
        parser.add_argument('service_ids', required=False, type=list, location='json')
        args = parser.parse_args()

        # Get current user ID from JWT token
        user_id = int(get_jwt_identity())

        # Fetch the booking to be updated
        booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
        if not booking:
            return {'message': 'Booking not found or you are not authorized to update this booking'}, 404

        # Update booking date if provided
        if args['booking_date']:
            try:
                booking_date = datetime.strptime(args['booking_date'], '%d/%m/%Y').date()
                booking.booking_date = booking_date
            except ValueError:
                return {'message': 'Invalid date format. Use DD/MM/YYYY.'}, 400

        # Update services if provided
        if args['service_ids']:
            # Clear existing services
            BookingService.query.filter_by(booking_id=booking_id).delete()
            # Fetch new services and calculate total cost
            service_ids = args['service_ids']
            services = Service.query.filter(Service.id.in_(service_ids)).all()
            if not services:
                return {'message': 'No valid services found.'}, 400

            total_cost = sum(service.cost for service in services)
            booking.total_cost = total_cost

            # Create new BookingService entries
            for service in services:
                booking_service = BookingService(booking_id=booking.id, service_id=service.id)
                db.session.add(booking_service)

        db.session.commit()

        return make_response(jsonify({'message': 'Booking updated successfully', 'booking_id': booking.id,'booking_date': booking.booking_date.strftime('%d/%m/%Y'),'total_cost': booking.total_cost}), 200)

customer_api.add_resource(UpdateBooking, '/booking/<int:booking_id>')



class DeleteBooking(Resource):

    @jwt_required()
    def delete(self, booking_id):
        # Get current user ID from JWT token
        user_id = int(get_jwt_identity())

        # Fetch the booking to be deleted
        booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
        if not booking:
            return {'message': 'Booking not found or you are not authorized to delete this booking'}, 404

        try:
            # Delete associated BookingService entries
            BookingService.query.filter_by(booking_id=booking.id).delete()

            # Delete the booking itself
            db.session.delete(booking)
            db.session.commit()

            return {'message': 'Booking deleted successfully', 'booking_id': booking.id}, 200

        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to delete booking', 'error': str(e)}, 500
customer_api.add_resource(DeleteBooking, '/booking/<int:booking_id>/delete')



