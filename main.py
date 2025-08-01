from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import base64

# Initialize the FastAPI app
app = FastAPI()

# POST endpoint to handle image upload and return the extracted portrait
@app.post("/extract-portrait/")
async def extract_portrait(file: UploadFile = File(...)):
    try:
        # Read the uploaded image file
        image_bytes = await file.read()

        # Convert bytes to a NumPy array for OpenCV processing
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Load the face detection model
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        # Convert the image to grayscale for better detection accuracy
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Try to find faces in the image
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) == 0:
            # No face found — return error message
            return JSONResponse(content={"error": "No face detected"}, status_code=400)

        # If multiple faces, just use the first one (assuming it's a portrait)
        (x, y, w, h) = faces[0]
        face_img = img[y:y+h, x:x+w]

        # Convert the cropped face into base64
        _, buffer = cv2.imencode('.jpg', face_img)
        face_b64 = base64.b64encode(buffer).decode('utf-8')

        return {"portrait_base64": face_b64}

    except Exception as e:
        # Catch unexpected errors and return as JSON
        return JSONResponse(content={"error": str(e)}, status_code=500)
