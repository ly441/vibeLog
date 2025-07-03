

# vibeLog

it about logging in moods and music according to what you are feeling,we are going to use spotify as our reference...

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
