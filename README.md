# E-commerce Web Application (Django)
This is a full-stack eCommerce web application built using Django.
The system allows users to browse products, place orders, and track delivery, while the admin manages products, stock, and delivery operations.

Features

User Side
User registration & login
Forgot password functionality
Browse products by category, subcategory, and sub-subcategory
Add to cart & wishlist
Place orders (Cash on Delivery / Online Payment)
Stock validation (prevents ordering out-of-stock products)


 Admin Side
Add / Edit / Delete products
Manage categories, subcategories, sub-subcategories
Set and monitor stock levels
View all orders
Assign orders to delivery boy


 Delivery Module
Separate login for delivery personnel
View assigned orders
Update order status (Delivered / Pending)


 Additional Features
Stock alert system (low stock & out-of-stock)
Order status tracking
Secure authentication system

Backend: Django (Python)
Database: SQLite
Frontend: HTML, CSS, Bootstrap
Payment Integration: Razorpay (Test Mode)


 Project Workflow
Admin adds products and sets stock
User browses and places an order
System validates stock and creates order
Admin assigns delivery boy
Delivery updates status
User tracks order
