# 2MEN | Premium Italian Fashion Store

A sophisticated E-commerce platform built with Django, dedicated to high-end Neapolitan sartorial excellence.

## 🚀 Features

- **Premium UI/UX**: Modern, minimalist design with smooth staggered animations and responsive layouts.
- **Dynamic Catalog**: Browse products by category (Shirts, Suits, Pants, Shoes) or Brand (Isaia, Kiton, Brunello Cucinelli).
- **Inventory Management**: Real-time stock tracking with size-specific availability and checkout validation.
- **Advanced Product Display**: Support for multiple images per product with a "Primary Image" selection feature.
- **Persistent Shopping Cart**: Session-based cart system allowing users to manage their items effortlessly.
- **Admin Dashboard**: Custom-configured Django Admin for professional inventory and order management.
- **Contact System**: Built-in contact form with AJAX submissions and email notifications.

## 🛠️ Tech Stack

- **Backend**: Python / Django
- **Database**: SQLite (Development)
- **Frontend**: HTML5, Vanilla CSS3 (Modern HSL colors, Glassmorphism), JavaScript (ES6+)
- **Icons**: Font Awesome 6

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SyedNajiullah/django-cloth-ordering.git
   cd django-cloth-ordering
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install django pillow
   ```

4. **Run Migrations**:
   ```bash
   cd core
   python manage.py migrate
   ```

5. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**:
   - Website: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

- `core/`: Main Django project configuration.
- `products/`: App handling product data, categories, and shopping cart logic.
- `static/`: Global CSS and JavaScript assets.
- `templates/`: HTML templates with base inheritance.
- `media/`: User-uploaded product images.

---
*Built with passion for Italian craftsmanship.*