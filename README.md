# AeroBuy E-Commerce Store 🛒

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg?style=flat-square)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.0+-green.svg?style=flat-square)](https://mongodb.com)

AeroBuy is a full-stack transactional e-commerce platform prototype featuring complete user accounts, dynamic product listing pages, robust shopping cart session persistence, checkout flows, and database order confirmations.

---

## 🎯 Architecture & Features
- **User Authentication**: Secure session-based signup, signin, and signout handlers.
- **Product Management**: Dynamic loading of items categorized by department (electronics, fashion, beauty, home) stored in MongoDB.
- **Persistent Shopping Cart**: In-memory Flask sessions for cart updates (add, modify, delete) synced with local order checkout.
- **Structured Database**: MongoDB collections for `users`, `products`, `orders`, and `checkouts`.

---

## 🛠️ Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript, jQuery, Bootstrap
- **Backend**: Python (Flask)
- **Database**: MongoDB (via `pymongo` client driver)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MongoDB installed locally and running on standard port `27017`

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rakeshgr962/AeroBuy.git
   cd AeroBuy
   ```

2. **Install python packages**:
   ```bash
   pip install Flask pymongo bcrypt
   ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```
   *AeroBuy will start running locally at `http://127.0.0.1:5000`.*

---

## 📂 Project Structure
```
AeroBuy/
├── app.py                      # Flask server routes and DB initializations
├── templates/                  # Frontend HTML views (home, cart, checkout, signin)
│   ├── home.html
│   ├── cart.html
│   ├── checkout.html.html
│   └── welcome.html
├── *.jpg / *.jpeg              # Product catalog image assets
└── README.md                   # Project documentation
```

---

## 📄 License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.
