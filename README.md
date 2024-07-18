# AutoAfya Backend

Welcome to the AutoAfya Backend repository! This project is a collaborative effort between Joanne Wendoh, Alvin Obala, and Arnold Kisuri. AutoAfya is a motor car servicing application designed to streamline the car maintenance process for users. This repository contains the backend code for the application, which is built using Flask.

## App was deployed and this is the live link: https://autoafya-backend-phase4-groupproject-iqky.onrender.com

## The frontend repo link: [AutoAfya Frontend](https://github.com/J-Wendoh/AutoAfya-FRONTEND-phase4-groupproject)

## Project Overview

AutoAfya is a web application that helps users schedule and manage car servicing appointments. The backend provides a robust API for handling data related to services, appointments, and user management.

## Features

- **User Management**: Register, login, and manage user profiles.
- **Service Management**: CRUD operations for car services.
- **Appointment Booking**: Schedule and manage car servicing appointments.
- **Service History**: View past and upcoming services for each user.

## Technologies Used

- **Flask**: Python microframework for building web applications.
- **SQLAlchemy**: ORM for managing database operations.
- **Marshmallow**: Library for object serialization and deserialization.
- **SQLite**: Lightweight database for development purposes.

## Getting Started

To get started with the AutoAfya backend project, follow these instructions:

### Prerequisites

Make sure you have the following software installed on your machine:

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository and navigate to the project directory:
    ```bash
    git clone https://github.com/J-Wendoh/AutoAfya-BACKEND-phase4-groupproject.git
    cd AutoAfya-BACKEND-phase4-groupproject
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

1. Set the Flask application environment variable:
    ```bash
    export FLASK_APP=app.py  # On Windows, use `set FLASK_APP=app.py`
    ```

2. Initialize the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

3. Start the development server:
    ```bash
    flask run
    ```

The API will be available at `http://localhost:5000`.

### API Endpoints

####Get all services:

URL: /customer/services
Method: GET
Get service by ID:

URL: /customer/services/<int:service_id>
Method: GET
Get reviews for a specific service:

URL: /customer/services/<int:service_id>/reviews
Method: GET

####Booking Endpoints:

Create or get bookings for the current user:

URL: /customer/booking
Method: POST or GET
Update a specific booking by ID:

URL: /customer/booking/<int:booking_id>
Method: PATCH
Delete a specific booking by ID:

URL: /customer/booking/<int:booking_id>/delete
Method: DELETE

####User Endpoints:

Fetch the username of the current user:
URL: /customer/username
Method: GET
Review Endpoints:
Create a review:

URL: /customer/review
Method: POST
Update a specific review by ID:

URL: /customer/review/<int:review_id>
Method: PATCH
Delete a specific review by ID:

URL: /customer/review/<int:review_id>/delete
Method: DELETE
Get all reviews:

URL: /customer/reviews/all
Method: GET
Get reviews by the current user:

URL: /customer/reviews/user
Method: GET


## Contributing

We welcome contributions to the AutoAfya backend project! To contribute, follow these steps:

1. Fork the repository: Create a personal fork of the repository on GitHub.
2. Clone your fork: Clone the forked repository to your local machine.
    ```bash
    git clone https://github.com/YOUR_USERNAME/AutoAfya-BACKEND-phase4-groupproject.git
    ```
3. Create a branch: Create a new branch for your feature or fix.
    ```bash
    git checkout -b feature/your-feature
    ```
4. Make changes: Implement your changes and test them.
5. Commit your changes: Commit your changes with a descriptive message.
    ```bash
    git add .
    git commit -m "Add feature: your-feature"
    ```
6. Push your changes: Push your changes to your forked repository.
    ```bash
    git push origin feature/your-feature
    ```
7. Create a Pull Request: Open a pull request on the main repository to merge your changes.

Please ensure that your code follows the existing code style and includes tests for any new features.

## Authors

This project is a group effort by:

- Joanne Wendoh - [GitHub](https://github.com/J-Wendoh)
- Alvin Obala - [GitHub](https://github.com/alvin-obala)
- Arnold Kisuri - [GitHub](https://github.com/arnold-kisuri)

## License

This project is licensed under the MIT License.

