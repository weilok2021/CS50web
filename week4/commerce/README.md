# 💰 E-Commerce Auction Platform

## Project Overview

Developed a **full-featured e-commerce auction web application** enabling users to create listings, place dynamic bids, and engage via comments. The application models a real-world auction site, integrating secure user management and complex logic to manage bidding and determine final winners.

This project was built to demonstrate proficiency in **full-stack web development** with a strong emphasis on architectural integrity and database interaction.

## ✨ Key Features

* **REST-style Routing:** The application uses clean, REST-style routing to manage resource access and manipulation.
* **Secure User Authentication:** Implemented user registration, login, and logout using **Django's built-in authentication system**.
* **Listing Management:** Authenticated users can create new auction listings with a title, description, starting bid, and category.
* **Dynamic Bidding Logic:** Users can place bids on active listings, with server-side validation ensuring bids are higher than the current highest bid.
* **Watchlist Functionality:** Users can add and remove listings from a personal watchlist for easy tracking.
* **Listing Closure:** The listing creator can close their auction, immediately declaring the highest bidder as the winner and preventing further bids.
---

## 💻 Technology Stack & Architecture

This platform leverages modern Python web technologies and follows established architectural patterns.

| Component | Technology | Role / Concept Demonstrated |
| :--- | :--- | :--- |
| **Backend Framework** | **Django** (Python) | Server-side logic, routing, and session management. |
| **Architecture** | **Model-View-Template (MVT)** | Decoupled structure separating data logic, presentation, and control flow. |
| **Database Modeling** | **Django ORM** (with **SQLite**) | Designed the database schema and managed data persistence efficiently without writing raw SQL. |
| **Data Interaction** | **REST-style API** | Clean, predictable URL routing and handling of all CRUD operations (Create, Read, Update, Delete). |
| **Frontend** | HTML, CSS (Bootstrap) | User interface and basic styling. |

---

## 🚀 Getting Started (Local Setup)

These instructions will get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.10+
* `pip` (Python package installer)

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/weilok2021/CS50web.git](https://github.com/weilok2021/CS50web.git)
    cd CS50web/week4/commerce
    ```

2.  **Create and Activate Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # .\venv\Scripts\activate # On Windows (Command Prompt)
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt 
    # Note: If requirements.txt is not available, install Django: pip install Django
    ```

4.  **Run Migrations:**
    ```bash
    python3 manage.py makemigrations auctions
    python3 manage.py migrate
    ```
    
5.  **Create Admin Account:**
    ```bash
    python3 manage.py createsuperuser
    # Note: superuser can login by /admin/ url of the application.
      Then you have the ability to add, modify, and delete any data 
      within the database through the admin interface.
    ```

6.  **Run the Server:**
    ```bash
    python3 manage.py runserver
    ```

The application will now be running on `http://127.0.0.1:8000/`.