import os
from app import create_app
from models import init_db

# 🔥 Add this print to confirm run.py is executing top-down
print("🛠️ Running init_db setup...")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "predictions.db")
init_db(DB_PATH)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
