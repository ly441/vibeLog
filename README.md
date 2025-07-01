# Vibelog API

A RESTful API for managing songs, moods, artists, and users for a late night TV show's playlist. Built with **Flask**, **PostgreSQL**, **SQLAlchemy**, and **JWT** authentication.

---

## Project Structure

```
vibeLog/
│
├── app.py                       
├── config.py                    
├── requirements.txt             
├── README.md                    
├── instance/
│   └── config.py                
├── migrations/                  
│
├── server/
│   ├── __init__.py              
│   │
│   ├── controllers/              
│   │   ├── artist_controller.py
│   │   ├── mood_controller.py
│   │   ├── song_controller.py
│   │   └── user_controller.py
│   │
│   ├── routes/                   

│   │   ├── artist.py
│   │   ├── mood.py
│   │   ├── song.py
│   │   └── user.py
│   │
│   ├── models/                  

│   │   ├── artist.py
│   │   ├── mood.py
│   │   ├── song.py
│   │   └── user.py
│   │
│   ├── db/
│   │   └── database.py          

│   │
│   └── auth/
│       └── auth.py               


---

## Tech Stack

- Python 3.x
- Flask
- PostgreSQL
- Flask-JWT-Extended
- Flask-Migrate
- SQLAlchemy
- python-dotenv

---

## Installation & Setup Instructions

Follow these steps to get the project running on your local machine.

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/ly441/vibeLog.git
cd vibeLog
```

---

### Step 2: Create Virtual Environment

```bash
python3 -m venv env
source env/bin/activate    # On Windows use: env\Scripts\activate
```

---

### Step 3: Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Create Environment Variables

1. In the root folder, create a `.env` file:

```bash
touch .env
```

2. Add the following environment variables:

```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
JWT_SECRET_KEY=your_secret_key_here
```

Replace `username`, `password`, and `your_database_name` with your actual PostgreSQL credentials.

---

### Step 5: Initialize and Migrate Database

```bash
flask db init            # Only once, to create migration folder
flask db migrate -m "Initial migration"
flask db upgrade
```

---

### Step 6: Run the Application

```bash
flask run
```

Access it at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Authentication & Authorization

You must register and log in to receive a JWT token.

---

### Register a User

```http
POST /register
Content-Type: application/json

{
  "username": "yourname",
  "email": "you@example.com",
  "password": "yourpassword"
}
```

---

### Log In

```http
POST /login
Content-Type: application/json

{
  "email": "you@example.com",
  "password": "yourpassword"
}
```

Response:

```json
{
  "access_token": "your-jwt-token"
}
```

Copy this token and include it in your headers:

```http
Authorization: Bearer your-jwt-token
```

---

## API Endpoints

> All `GET`, `POST`, `PUT`, and `DELETE` routes (except register/login) require a JWT token.

| Method | Endpoint          | Description             |
|--------|-------------------|-------------------------|
| POST   | `/register`       | Register a new user     |
| POST   | `/login`          | Login and get JWT       |
| GET    | `/songs`          | Get all songs           |
| POST   | `/songs`          | Create a new song       |
| PUT    | `/songs/<id>`     | Update song by ID       |
| DELETE | `/songs/<id>`     | Delete song by ID       |
| GET    | `/artists`        | List all artists        |
| POST   | `/artists`        | Add an artist           |
| GET    | `/moods`          | List all moods          |
| POST   | `/moods`          | Add a new mood          |

Use Postman or Insomnia to test these endpoints.

---

## Testing API with Postman

1. Import your endpoints into Postman.
2. Add a `POST /login` call and obtain a token.
3. Go to "Authorization" tab → select `Bearer Token` and paste your token.
4. Test all secure endpoints (like `/songs`, `/artists`, etc.).

---

## Project Links

- GitHub Repository: [https://github.com/ly441/vibeLog](https://github.com/ly441/vibeLog)  
- Google Slides Presentation: [View Presentation](https://docs.google.com/presentation/d/1HTN21mQ7qEzAMWkq-I-mHeVxY_bJcFMYUIRdikMRe7o/edit?usp=sharing)

---

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025
Lynn Kolii, Felix Mwangi, Everlyn Simiyu, Abdiwelli Omar, Silvester Ngaruiya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## Authors

- Lynn Kolii  
- Felix Mwangi  
- Everlyn Simiyu  
- Abdiwelli Omar  
- Silvester Ngaruiya

 One attachment
  •  Scanned by Gmail
Attachment scanning in Gmail
To help protect your inbox, Gmail blocks attachments when malware is detected. You should still only download attachments from people you trust. Learn more
Safer with Google logo
Thanks, I'll check it out.Thanks for the tip!What is this?


