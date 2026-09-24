# Importing the required libraries
from flask import Flask,render_template,request,redirect, url_for
#import mysql.connector


app = Flask(__name__)

import sqlite3

mydb = sqlite3.connect("fish.db", check_same_thread=False)
mydb.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT)")
mydb.commit()
mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query.replace("%s", "?"),values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query.replace("%s", "?"),values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home', methods=["POST", "GET"])
def home():
    return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email.upper() in email_data_list:
            
            query = "SELECT UPPER(password) FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password.upper() == password__data[0][0]:
                
                global user_email
                user_email = email

                return render_template('home.html')
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']  

        if password != c_password:
            return render_template('register.html', message="Confirm password does not match!")

        
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_data_list = [i[0] for i in email_data]

        if email.upper() in email_data_list:
            return render_template('register.html', message="This email ID already exists!")

        
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, password)
        executionquery(query, values)

        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')


# from flask import Flask, render_template, request
# from ultralytics import YOLO
# import cv2
# import os
# import numpy as np
# import base64


# app.config['UPLOAD_FOLDER'] = 'static/uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# MODEL_PATH = "model.pt" 
# model = YOLO(MODEL_PATH)

# @app.route('/prediction', methods=['GET', 'POST'])
# def prediction():
#     # Default values for GET request
#     result_image = None
#     detections = []
#     original_image_url = None

#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return render_template('prediction.html', error="No file uploaded")

#         file = request.files['file']
#         if file.filename == '':
#             return render_template('prediction.html', error="No file selected")

#         # Read and decode image
#         filestr = file.read()
#         npimg = np.frombuffer(filestr, np.uint8)
#         img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#         if img is None:
#             return render_template('prediction.html', error="Invalid or corrupted image")

#         # Save original for display
#         original_b64 = base64.b64encode(filestr).decode('utf-8')
#         original_image_url = f"data:image/jpeg;base64,{original_b64}"

#         # Run YOLO inference
#         results = model(img, conf=0.25, iou=0.45, verbose=False)

#         # Collect detections and draw boxes
#         detections = []
#         for r in results:
#             for box in r.boxes:
#                 cls_id = int(box.cls[0].item())
#                 conf = round(float(box.conf[0].item()), 3)
#                 name = model.names[cls_id]

#                 detections.append({
#                     "name": name,
#                     "confidence": conf,
#                     "confidence_percent": round(conf * 100, 1)
#                 })

#                 # Draw bounding box and label
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 label = f"{name} {conf:.2f}"
#                 cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
#                 cv2.putText(img, label, (x1, y1 - 10),
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

#         # Encode result image to base64
#         _, buffer = cv2.imencode('.jpg', img)
#         result_b64 = base64.b64encode(buffer).decode('utf-8')
#         result_image = f"data:image/jpeg;base64,{result_b64}"

#     # Always render prediction.html (with or without results)
#     return render_template(
#         'prediction.html',
#         result_image=result_image,
#         original_image=original_image_url,
#         detections=detections,
#         has_result=(request.method == 'POST' and result_image is not None)
#     )

from flask import Flask, render_template, request
from ultralytics import YOLO
import cv2
import os
import numpy as np
import base64

app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MODEL_PATH = "model.pt" 
model = YOLO(MODEL_PATH)

# Species information – keys should match model.names exactly (case sensitive)
# We use .lower() later to make matching more forgiving
FISH_INFO = {
    "anabas": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Widely distributed and hardy species.",
        "benefits": "Good source of protein. Traditionally valued in some regions for post-illness recovery."
    },
    "bangus": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Common milkfish – aquaculture is sustainable.",
        "benefits": "Rich in protein, omega-3 fatty acids, good for heart and brain health."
    },
    "black spotted barb": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Abundant in many freshwater systems.",
        "benefits": "Protein-rich small fish, often eaten whole (good calcium source)."
    },
    "clarias": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Very common, widely farmed.",
        "benefits": "High protein, affordable nutrition, good source of iron."
    },
    "clownfish": {
        "eatable": "No (ornamental)",
        "status": "Least Concern",
        "preservation": "Protected in coral reefs – not a food fish.",
        "benefits": "Not consumed – aquarium species."
    },
    "common silver carp": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Widely farmed worldwide.",
        "benefits": "Lean protein, low fat, rich in omega-3s."
    },
    "fighting fish": {
        "eatable": "No",
        "status": "Least Concern (bred varieties)",
        "preservation": "Ornamental only.",
        "benefits": "Not a food fish."
    },
    "nile tilapia": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "One of the most farmed fish globally.",
        "benefits": "High-quality lean protein, vitamin B12, selenium – good for muscle & heart."
    },
    "pangasiidae": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Intensive farming common – choose responsible sources.",
        "benefits": "Good protein, low calories when well-managed."
    },
    "rainbowfish": {
        "eatable": "No",
        "status": "Varies by species",
        "preservation": "Mostly ornamental.",
        "benefits": "Not consumed."
    },
    "red tilapia fish": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Widely farmed.",
        "benefits": "Lean protein, heart-friendly, good source of phosphorus."
    },
    "silver angelfish": {
        "eatable": "No",
        "status": "Least Concern (ornamental)",
        "preservation": "Aquarium fish – not for consumption.",
        "benefits": "Not applicable."
    },
    "siriped catfish": {
        "eatable": "Yes",
        "status": "Least Concern / Near Threatened (some regions)",
        "preservation": "Monitor local overfishing.",
        "benefits": "Protein-rich, good flavor in many preparations."
    },
    "spotted featherback": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Common in many areas.",
        "benefits": "Good protein, unique texture."
    },
    "tilapia": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Very sustainable through farming.",
        "benefits": "Lean, high protein, low fat – supports muscle health."
    },
    "aair": {
        "eatable": "Yes",
        "status": "Least Concern / some Near Threatened",
        "preservation": "Common in many freshwater bodies.",
        "benefits": "Protein-rich, popular in local cuisine."
    },
    "boal": {
        "eatable": "Yes (moderation advised)",
        "status": "Vulnerable (many regions)",
        "preservation": "Avoid overfishing; support habitat protection.",
        "benefits": "High protein, flavorful – good for muscle building."
    },
    "catfish": {
        "eatable": "Yes",
        "status": "Least Concern (most species)",
        "preservation": "Many farmed sustainably.",
        "benefits": "Rich in protein, omega-3s in some varieties."
    },
    "chapila": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Abundant small fish.",
        "benefits": "Good protein and micronutrients."
    },
    "deshi puti": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "No major concern.",
        "benefits": "Small fish – rich in calcium when eaten whole."
    },
    "foli": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Common featherback species.",
        "benefits": "Protein-rich, good in curries."
    },
    "goldfish": {
        "eatable": "No (ornamental)",
        "status": "Least Concern",
        "preservation": "Not consumed – pet fish.",
        "benefits": "Not applicable."
    },
    "ilish": {
        "eatable": "Yes (very popular)",
        "status": "Near Threatened / Vulnerable (wild populations)",
        "preservation": "Follow seasonal bans, support sustainable fishery.",
        "benefits": "Extremely rich in omega-3, protein, vitamin A & D – excellent for heart & brain."
    },
    "kal baush": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Common local species.",
        "benefits": "Good protein source."
    },
    "katla": {
        "eatable": "Yes",
        "status": "Least Concern (widely farmed)",
        "preservation": "Sustainable through aquaculture.",
        "benefits": "Lean protein, omega-3s – good for heart & joints."
    },
    "koi": {
        "eatable": "No (ornamental)",
        "status": "Least Concern (bred varieties)",
        "preservation": "Not a food fish.",
        "benefits": "Ornamental use only."
    },
    "magur": {
        "eatable": "Yes",
        "status": "Least Concern / some Near Threatened",
        "preservation": "Farmed varieties sustainable.",
        "benefits": "High protein, helps with energy & anemia."
    },
    "mrigel": {
        "eatable": "Yes",
        "status": "Least Concern (cultured)",
        "preservation": "Common in composite fish culture.",
        "benefits": "Excellent protein & omega-3 source."
    },
    "pabda": {
        "eatable": "Yes",
        "status": "Near Threatened (some decline)",
        "preservation": "Support sustainable practices.",
        "benefits": "Delicate taste, good protein & fats."
    },
    "pangas": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Intensive farming – choose good sources.",
        "benefits": "Affordable protein, versatile cooking."
    },
    "puti": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Very common small fish.",
        "benefits": "High calcium (eaten whole), protein & micronutrients."
    },
    "rui": {
        "eatable": "Yes",
        "status": "Least Concern (farmed extensively)",
        "preservation": "Widely cultivated – no major concern.",
        "benefits": "Rich protein, omega-3, vitamins – great for heart & immunity."
    },
    "shol": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Resilient species.",
        "benefits": "High protein, low fat – valued in recovery diets."
    },
    "taki": {
        "eatable": "Yes",
        "status": "Least Concern",
        "preservation": "Hardy and widespread.",
        "benefits": "Good protein, traditional medicinal value in some cultures."
    },
    # Fallback
    "unknown": {
        "eatable": "Check species",
        "status": "Varies",
        "preservation": "Follow local fishing rules & conservation guidelines.",
        "benefits": "Most freshwater fish offer good protein and essential nutrients."
    }
}

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    result_image = None
    detections = []           # ← this will now contain **unique** species
    original_image_url = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('prediction.html', error="No file part")

        file = request.files['file']
        if file.filename == '':
            return render_template('prediction.html', error="No selected file")

        # Read image
        filestr = file.read()
        npimg = np.frombuffer(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return render_template('prediction.html', error="Invalid image")

        # Original for display
        original_b64 = base64.b64encode(filestr).decode('utf-8')
        original_image_url = f"data:image/jpeg;base64,{original_b64}"

        # YOLO inference
        results = model(img, conf=0.25, iou=0.45, verbose=False)

        # ────────────────────────────────────────────────
        # Group by species name → keep highest confidence
        # ────────────────────────────────────────────────
        from collections import defaultdict

        species_data = defaultdict(lambda: {
            "max_conf": 0.0,
            "count": 0,
            "name": ""
        })

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                name = model.names[cls_id]
                name_lower = name.lower().strip()

                # Update stats
                if conf > species_data[name_lower]["max_conf"]:
                    species_data[name_lower]["max_conf"] = conf
                    species_data[name_lower]["name"] = name  # keep original case

                species_data[name_lower]["count"] += 1

                # Still draw EVERY box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"{name} {conf:.2f}"
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(img, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Prepare final list for template (unique species)
        detections = []
        for lower_name, data in species_data.items():
            info = FISH_INFO.get(lower_name, FISH_INFO["unknown"])

            detections.append({
                "name": data["name"],                     # original case
                "confidence": round(data["max_conf"], 3),
                "confidence_percent": round(data["max_conf"] * 100, 1),
                "count": data["count"],
                "eatable": info["eatable"],
                "status": info["status"],
                "preservation": info["preservation"],
                "benefits": info["benefits"]
            })

        # Sort by confidence descending (most confident first)
        detections.sort(key=lambda x: x["confidence"], reverse=True)

        # Encode result image
        _, buffer = cv2.imencode('.jpg', img)
        result_b64 = base64.b64encode(buffer).decode('utf-8')
        result_image = f"data:image/jpeg;base64,{result_b64}"

    return render_template(
        'prediction.html',
        result_image=result_image,
        original_image=original_image_url,
        detections=detections,
        has_result=(request.method == 'POST' and result_image is not None)
    )


@app.route('/camera')
def camera():
    return render_template("camera.html")

@app.route('/predict_frame', methods=['POST'])
def predict_frame():
    img = cv2.imdecode(np.frombuffer(request.get_data(), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return "Invalid image", 400
    for box in model(img, conf=0.3, verbose=False)[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        label = f"{model.names[int(box.cls[0])]} {float(box.conf[0]):.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(img, label, (x1, max(y1 - 8, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return cv2.imencode('.jpg', img)[1].tobytes(), 200, {'Content-Type': 'image/jpeg'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
