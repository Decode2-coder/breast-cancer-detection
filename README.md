Breast Cancer Detection using Federated Learning and Blockchain
📝 Project Description
This project develops a secure, privacy-preserving AI system for breast cancer detection, utilizing federated learning across multi-modal medical datasets (histopathology, mammography, ultrasound).
The system integrates blockchain-based authentication using MetaMask and Web3.js for decentralized user management, ensuring data privacy and security.

🚀 Features
Federated learning across separate datasets without raw data sharing

Real-time cancer prediction with confidence score visualization

Blockchain-based authentication (MetaMask wallet login)

TensorFlow (TFSMLayer) model deployed using Flask

Chart.js-based confidence visualization

Secure report download functionality

🖥️ Tech Stack
Frontend: HTML, CSS, JavaScript (Jinja2 templating)


Backend: Flask, TensorFlow (Keras 3.x), Web3.py


Blockchain Integration: MetaMask, Web3.js


Database: SQLite (for prediction logs)


Other Tools: Chart.js for visualization, TFSMLayer for TensorFlow SavedModel loading

⚙️ Installation
Clone the repository:

git clone https://github.com/yourusername/breast-cancer-detection.git

cd breast-cancer-detection

Create a virtual environment:

python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`


Install dependencies:

pip install -r requirements.txt


Run the application:
python run.py
🔐 Prerequisites
MetaMask browser extension installed

Localhost running Flask server (http://127.0.0.1:5000)
