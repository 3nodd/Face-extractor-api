
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import cv2
import numpy as np
import base64
from io import BytesIO

app = FastAPI()

@app.post("/extract-portrait/")
async def extract_portrait(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image or no image data found.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            raise HTTPException(status_code=422, detail="No face detected in the image.")

        x, y, w, h = faces[0]
        cropped_face = img[y:y+h, x:x+w]

        _, buffer = cv2.imencode('.jpg', cropped_face)
        portrait_base64 = base64.b64encode(buffer).decode('utf-8')

        return {
            "portrait_base64": portrait_base64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract-portrait/image/")
async def extract_portrait_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image or no image data found.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            raise HTTPException(status_code=422, detail="No face detected in the image.")

        x, y, w, h = faces[0]
        cropped_face = img[y:y+h, x:x+w]

        _, buffer = cv2.imencode('.jpg', cropped_face)
        return StreamingResponse(BytesIO(buffer), media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
