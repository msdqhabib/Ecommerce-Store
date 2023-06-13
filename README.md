# Ecommerce-Store-using-Django

👋 The project aims to provide a web-based platform for users to browse, purchase, and manage products online. It includes features such as shopping carts, categories, user accounts (login, logout, signup), orders, and a store.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- system allows users to create accounts, log in, log out, and manage their personal information.
- store displays product details, pricing information, and availability.
- Users can place orders for the products they want to purchase and view their order history.
- Users can add products to their shopping carts, update quantities, and remove items.

## Installation

To get started with Ecommerce store, you need to have Python and pip installed on your system. Then, follow these steps:

1. Clone this repository:
```python
git clone https://github.com/msdqhabib/Ecommerce-Store.git
```
2. Navigate to the project directory:
```python
cd Ecommerce-store
```
3. Install the required packages:
```python
pip install -r requirements.txt
```
4. Apply the database migrations:
```python
python manage.py migrate
```
5. Create a superuser account:
```python
python manage.py createsuperuser
```
6. Run the development server:
```python
python manage.py runserver
```

The application will now be available at `http://localhost:8000`.

## Usage

To use Ecommerce store, open your web browser and go to `http://localhost:8000`. From there, you can sign up or log in to your account, add products to cart, and search for specific products or filter products by category.

## Contributing

If you would like to contribute to Ecommerce Store, you can follow these steps:

1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Write your code and add tests if possible.
4. Submit a pull request.

## License

Ecommerce Store is licensed under the MIT License. See [LICENSE](LICENSE) for more information.