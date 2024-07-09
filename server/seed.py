#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    User.query.delete()

    fake = Faker()

    print("Creating users...")

    # make sure users have unique usernames
    users = []
    usernames = set()

    for i in range(20):

        username = fake.first_name().lower()  # Ensure lowercase usernames
        while username in usernames:
            username = fake.first_name().lower()
        usernames.add(username)

        user = User(
            username=username,
            email= fake.email(),
            image_url=fake.url(),
        )

        user.password_hash = user.username + 'password'

        users.append(user)

    db.session.add_all(users)


    try:
        db.session.add_all(users)
        db.session.commit()
        print("Complete.")
    except Exception as e:
        print(f"Error creating users: {e}")
        db.session.rollback()  # Rollback on error

