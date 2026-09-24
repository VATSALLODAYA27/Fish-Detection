# Fish Detection in Marine Environments (YOLO Object Detection)

A Flask web app that uses a YOLO model to detect fish in an uploaded image (or a live webcam feed) and identify the species, along with basic info (is it eatable, conservation status, health benefits).

## How the dataset connects to the model

1. **Source dataset** — the training images and species labels come from the Roboflow dataset:
   `https://universe.roboflow.com/kittiphone-phouthavong-4tt12/fish-e7im9`
   (combined with an additional freshwater/Bangladeshi fish dataset — that's why the class list mixes names like `Nile Tilapia`, `Clownfish` with names like `ilish`, `rui`, `katla`).
2. **Training happens outside this app.** Roboflow (or the training scripts under `CODE/BACKEND/YOLO11` and `CODE/BACKEND/YOLOV9`) is used to train a YOLO model on that labeled dataset. Training produces a weights file — that file is `model.pt` in this folder.
3. **`model.pt` is the only link this app needs to the dataset.** The app never talks to Roboflow at runtime — it just loads `model.pt` with `ultralytics.YOLO('model.pt')` (see `app.py`). The class-name → species mapping the dataset defined during training is baked into the weights file itself, and is retrieved at inference time via `model.names`.
4. **The 35 species the current `model.pt` recognizes:**
   `Anabas, Bangus, Black Spotted Barb, Clarias, Clownfish, Common Silver Carp, Fighting Fish, Nile Tilapia, Pangasiidae, Rainbowfish, Red Tilapia Fish, Silver Angelfish, Siriped Catfish, Spotted Featherback, Tilapia, aair, boal, catfish, chapila, deshi puti, foli, goldfish, ilish, kal baush, katla, koi, magur, mrigel, pabda, pangas, puti, rui, shol, taki, tara baim`

## How an uploaded image gets identified as "this fish"

This is handled in the `/prediction` route in `app.py`:

1. You upload an image on the **Prediction** page. Flask reads the file into memory and decodes it with OpenCV (`cv2.imdecode`).
2. The image is passed to the loaded YOLO model: `model(img, conf=0.25, iou=0.45)`.
   - The model scans the image and returns one or more **bounding boxes**, each with a **class id** (which species) and a **confidence score**.
3. For each detected box:
   - The class id is converted to a species name via `model.names[cls_id]`.
   - A green rectangle + label (`species name + confidence`) is drawn on the image with `cv2.rectangle` / `cv2.putText`.
4. If the same species is detected multiple times in the image, only the **highest-confidence** detection is kept for the results table (but every box is still drawn on the image).
5. Each detected species name is looked up in the `FISH_INFO` dictionary (also in `app.py`) to attach:
   - `eatable` — Yes / No / ornamental
   - `status` — conservation status (e.g. Least Concern, Near Threatened)
   - `preservation` — sustainability notes
   - `benefits` — nutritional/health info
   - If a detected class isn't in `FISH_INFO`, it falls back to a generic `"unknown"` entry.
6. The original image, the annotated (boxed) image, and the results table are all sent back to `prediction.html` and rendered — that's how the page tells you "this is a *Rui*" (or whichever species) along with confidence % and the extra info.

The **live camera** page (`/camera`) uses your browser webcam: the page sends a frame to `/predict_frame` about 3 times a second and shows the returned image with boxes drawn. `live1.py` is the older standalone OpenCV-window version and is not used by the web app.

## Project structure (this folder)

```
FRONTEND/
├── app.py            Flask app: routes for home/login/register/prediction/camera
├── live1.py           Standalone webcam live-detection script (opens its own OpenCV window)
├── model.pt            Trained YOLO weights (the "dataset connection")
├── db.sql               Old MySQL schema (unused; the app now creates a SQLite `fish.db` itself)
├── req.txt                Original package list this project was built with
├── templates/           HTML pages (index, home, login, register, prediction, camera, about)
└── static/                CSS/JS/uploads
```

## Steps to run the app

### 1. Prerequisites
- Python 3.10+ (no database server needed; users are stored in a local SQLite file `fish.db`, created on first run)

### 2. Create a virtual environment and install dependencies
```bash
python -m venv .venv
.venv\Scripts\activate
pip install flask ultralytics opencv-python numpy
```
(`ultralytics` pulls in `torch`/`torchvision` automatically — first install can take a few minutes.)

### 3. Run the app
```bash
python app.py
```
Flask will start on **http://127.0.0.1:5000**. Open that URL in a browser.

### 4. Use it
- **Home / About** — landing pages.
- **Register / Login** — create an account, stored in the `users` table.
- **Prediction** — upload a fish image; the annotated image + species info table is shown.
- **Camera** — click Start and allow camera access; detections are drawn live in the page.

### Notes
- Passwords are stored in plain text in `fish.db` — fine for a demo, not for production.
- The `static/uploads` folder is created automatically on first run if it doesn't exist.
