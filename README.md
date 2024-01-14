# Greatkart an E-Commerce Website

Welcome to our E-Commerce website! This project is designed to provide a seamless online shopping experience, featuring session management, user authentication, email verification, PayPal payment integration, a session-based shopping cart, and a review rating system.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)


## Features

1. **User Authentication:** Secure sign-up, sign-in, and password recovery with email verification.

2. **Session Management:** Persistent user sessions for a personalized shopping experience.

3. **PayPal Integration:** Secure and convenient payment processing using PayPal.

4. **Shopping Cart:** Session-based shopping cart to add, update, and remove items.

5. **Review Rating System:** Customers can leave reviews and rate products.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.9 or later: [Download here](https://www.python.org/downloads/release/python-390/)

## Installation

Follow these steps to set up the Car Selling Website on your local machine:

```bash```
# Clone the repository
git clone https://github.com/ripnoob/shop

# Open terminal & go to project directory
cd shop

# Create virtual env
python -m venv env
&& source env/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Run project
python manage.py makemigrations &&
python manage.py migrate && python manage.py runserver
