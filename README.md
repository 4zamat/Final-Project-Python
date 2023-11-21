# Final-Project-Python
Azamat, Arafat and Danial's python final project
KEY FEATURES:
1.	User Registration and Authentication:
●	Users can register with the system by providing necessary details such as username, first name, last name, and password.
●	The system should handle password confirmation and ensure unique usernames.
●	User authentication will be implemented using Flask-Login.
2.	User Profile:
●	Registered users can view their profiles.
●	Profiles should display user information and booking history.
●	User authentication should be implemented to ensure users can only access their own profiles.
3.	Movie Booking:
●	Users can select a movie and book tickets for specific showtimes.
●	Implement a booking mechanism that associates bookings with users.




4.	Admin Dashboard:
●	Admins can access a dashboard to manage user accounts and movie information.
●	Admins should be able to add, update, or delete movies from the system.
●	User management features include viewing user details, updating information, and deleting user accounts.


TECHNOLOGY STACK:
Web Framework: Flask
Database: SQLAlchemy (integrated with Flask)
User Authentication: Flask-Login
Frontend: HTML, CSS, JavaScript (Jinja2 templating)
Deployment: Flask development server for testing

PROJECT GOALS:
User-Friendly Interface: Create a responsive and intuitive user interface for easy navigation.
Security: Implement secure user authentication and protect against common web vulnerabilities.
Code Quality: Follow best practices for Flask development, including modular code structure and proper error handling.
Testing: Conduct thorough testing of the application, including unit tests for critical functionalities.




PROJECT STRUCTER:
main.py: Main application file containing route definitions.
templates/: Folder containing HTML templates for different pages.
database/: Module for defining and interacting with the database models.
flaskapp/: Module for initializing Flask and Flask-Login.

FUTURE ENHANCEMENTS:
Payment Integration: Integrate a payment gateway for online ticket booking.
Email Notifications: Implement email notifications for booking confirmations and account-related activities.
Movie Reviews: Allow users to submit reviews for movies.
Localization: Add support for multiple languages.

CONCLUSION
The Movie Booking and User Management System will provide a comprehensive solution for managing movie bookings and user accounts. The project will be developed iteratively, with continuous testing and feedback to ensure a robust and user-friendly application.

