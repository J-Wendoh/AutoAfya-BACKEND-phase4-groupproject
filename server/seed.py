#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, User, Service

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    User.query.delete()
    Service.query.delete()  # Add this line to delete existing services

    print("Creating users...")

    # Make sure users have unique usernames
    users = []
    usernames = set()

    for i in range(10):
        username = fake.first_name().lower()  # Ensure lowercase usernames
        while username in usernames:
            username = fake.first_name().lower()
        usernames.add(username)

        user = User(
            username=username,
            email=fake.email(),
            password=fake.password()  # Generate a random password
        )

        users.append(user)

    db.session.add_all(users)

    print("Creating services...")

    service_names = [
        "Oil Change", "Brake Inspection", "Tire Rotation", "Battery Check",
        "Wiper Blade Replacement", "Wheel Alignment", "Transmission Service"
    ]

    services = []

    for name in service_names:
        service = Service(
            name=name,
            description=fake.text(max_nb_chars=80),
            cost=round(fake.random_number(digits=2) + fake.random.random(), 2)  # Generate a random cost
        )
        services.append(service)

    db.session.add_all(services)

    try:
        db.session.commit()
        print("Complete.")
    except Exception as e:
        print(f"Error creating records: {e}")
        db.session.rollback()  # Rollback on error
