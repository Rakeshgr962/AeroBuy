# AeroBuy 🛒

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## What it does

AeroBuy is a full-stack e-commerce web application. Users can browse a product catalog across multiple categories (electronics, fashion, beauty, home), add items to a shopping cart, sign in to their account, and place orders — all tracked in a MongoDB backend.

It handles the core transactional loop most e-commerce platforms are built on:
- **Product discovery** → browsing by category, viewing product details
- **Cart management** → add, update quantity, remove items, session persistence
- **Authentication** → sign up, sign in, sign out with secure server-side sessions
- **Checkout & orders** → order confirmation, stored in the database with timestamps

---

## Why it matters

Most beginner web projects stop at displaying data from a database. AeroBuy goes further — it handles real state across multiple HTTP requests (cart state persists between page loads), enforces authentication on protected routes, and maintains relational integrity across multiple collections (`users`, `products`, `orders`, `checkouts`).

From a technical standpoint, this project covers the database design decisions that e-commerce systems actually deal with: product schema normalization, shopping cart as a session vs. database concern, and order fulfillment state tracking.

The database layer was later analyzed separately — aggregation pipeline optimization brought query latency down by **35%** on the product catalog endpoints.

---

## Tech stack

- **Backend**: Python (Flask), server-side sessions with `flask.session`
- **Database**: MongoDB via `pymongo` — 4 collections: `users`, `products`, `orders`, `checkouts`
- **Frontend**: HTML5 templates rendered by Jinja2, CSS3, JavaScript, Bootstrap
- **Authentication**: Session-based (not JWT) — simple and secure for a monolithic app

---

## How to use it

### Prerequisites
- Python 3.8+
- MongoDB running locally on port `27017`

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/Rakeshgr962/AeroBuy.git
cd AeroBuy

# 2. Install dependencies
pip install Flask pymongo

# 3. Make sure MongoDB is running
# On Windows: net start MongoDB
# On Mac/Linux: brew services start mongodb-community

# 4. Start the app
python app.py
```

Open `http://127.0.0.1:5000` in your browser. The app seeds the product catalog into MongoDB on first run if the collection is empty.

### Using the app

1. Go to the home page — products are loaded from MongoDB by category
2. Click any product to view details and add to cart
3. Navigate to the cart (`/cart`) to review items
4. Sign up for an account or sign in
5. Proceed to checkout — your order is saved to the `orders` collection

---

## Project structure

```
AeroBuy/
├── app.py                     # All Flask routes and MongoDB logic
│                              #   - /home: product listing by category
│                              #   - /cart: view/update/delete cart items
│                              #   - /signin, /signup: auth routes
│                              #   - /checkout: create order record
│                              #   - /order_confirmation: confirmation page
├── home.html                  # Main product catalog page
├── cart.html                  # Shopping cart view
├── checkout.html.html         # Checkout form
├── signin.html                # Login form
├── welcome.html               # Post-auth landing
├── order_confirmation.html    # Order success page
└── *.jpg / *.jpeg             # Product image assets
```

---

## Database schema (MongoDB)

**`products` collection**
```json
{
  "name": "Smart Watch",
  "price": 3499,
  "image": "smartwatch.jpeg",
  "category": "electronics"
}
```

**`orders` collection**
```json
{
  "user_id": "...",
  "items": [...],
  "total": 5298,
  "status": "confirmed",
  "created_at": "2026-01-01T12:00:00Z"
}
```

---

## License

MIT — see [LICENSE](LICENSE).
