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

Screenshots
<img src="https://github.com/user-attachments/assets/4ce0fc93-bfce-4edf-867d-324dea6920d1" width="500" />
<img src="https://github.com/user-attachments/assets/bd986c69-0684-40a5-b80d-44fee40c138e" width="500" />
<img src="https://github.com/user-attachments/assets/3cd34866-a734-428e-a8f8-ff09d9dd4cd5" width="500" />
 <img src="https://github.com/user-attachments/assets/6f8c9e74-4270-4348-90e1-81e8562623e1" width="500" />
<img src="https://github.com/user-attachments/assets/24698621-da81-4358-8156-1fca1322bdcb" width="500" />
 
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
