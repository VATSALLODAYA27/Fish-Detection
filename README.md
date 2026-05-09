# 🐟 Fish Detection and Classification System

## 📌 Project Overview

This project is an AI-powered Fish Detection and Classification System developed using Deep Learning and Computer Vision techniques. The system is designed to identify and classify different fish species from images and live camera feeds using the YOLOv9 object detection model.

The project combines a Flask-based web application with a trained YOLO model to provide real-time fish detection functionality. It can be used in marine research, fisheries management, underwater monitoring, and educational applications.

---

# 🚀 Features

* ✅ Fish detection using YOLOv9
* ✅ Real-time camera detection support
* ✅ Image upload and prediction
* ✅ User authentication system (Login/Register)
* ✅ Flask-based web interface
* ✅ MySQL database integration
* ✅ Detection result visualization
* ✅ Test case image support

---

# 🛠️ Technologies Used

## Frontend

* HTML
* CSS
* JavaScript
* Bootstrap

## Backend

* Python
* Flask

## Database

* MySQL

## AI / Deep Learning

* YOLOv9
* TensorFlow
* OpenCV
* NumPy
* Pandas

---

# 📂 Project Structure

```bash
FISH PROJECT/
│
├── CODE/
│   ├── BACKEND/
│   │   └── YOLOV9/
│   │       ├── results.png
│   │       ├── confusion_matrix.png
│   │       ├── train_batch0.jpg
│   │       └── ...
│   │
│   └── FRONTEND/
│       ├── templates/
│       ├── static/
│       ├── Test Cases/
│       ├── app.py
│       ├── live1.py
│       ├── db.sql
│       └── req.txt
│
└── README.md
```

---

# ⚙️ Installation and Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/fish-detection-system.git
cd fish-detection-system
```

---

## 2️⃣ Create Virtual Environment (Optional)

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r req.txt
```

---

# 📦 Required Libraries

```txt
tensorflow==2.16.1
ultralytics==8.3.189
numpy==1.26.4
opencv-python==4.12.0.88
Flask==3.0.3
pandas==2.3.2
mysql-connector-python==9.4.0
```

---

# 🗄️ Database Setup

1. Open MySQL
2. Create a database named:

```sql
CREATE DATABASE fish;
```

3. Import the `db.sql` file.

4. Update MySQL credentials inside `app.py`

```python
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    port=3306,
    database="fish"
)
```

---

# ▶️ Run the Project

```bash
python app.py
```

Then open:

```bash
http://127.0.0.1:5000/
```

---

# 📸 System Modules

## 🔹 User Authentication

* User Registration
* User Login
* Session Management

## 🔹 Fish Detection

* Upload fish image
* Detect fish species
* Display prediction results

## 🔹 Live Detection

* Real-time camera-based detection
* Instant object tracking and recognition

---

# 📊 Model Information

* Model Used: YOLOv9
* Framework: Ultralytics
* Detection Type: Object Detection
* Training Dataset: Fish Image Dataset

The model is trained to detect and classify multiple fish species with high accuracy.

---

# 📈 Output Results

The backend folder contains:

* Confusion Matrix
* Precision Curves
* Validation Prediction Images
* Training Batch Results
* Detection Result Graphs

These outputs help evaluate the model performance.

---

# 🧪 Test Cases

The project includes multiple sample test images inside:

```bash
CODE/FRONTEND/Test Cases/
```

You can use these images to test the detection model.

---

# 🔮 Future Enhancements

* Multi-species fish tracking
* Underwater video analytics
* Mobile application integration
* Cloud deployment
* Improved detection accuracy
* Real-time dashboard analytics

---

# 👨‍💻 Author

## Vatsal Hitesh Lodaya

B.Tech Computer Engineering (Honours in Data Science)

---

# 📜 License

This project is developed for educational and research purposes.

---

# ⭐ GitHub Support

If you like this project, consider giving it a ⭐ on GitHub.
