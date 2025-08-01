from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import cv2
import numpy as np
import base64
import io

app = FastAPI(title="Face Extractor API")

@app.post("/extract-portrait/")
async def extract_portrait(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        raise HTTPException(status_code=404, detail="No face found")

    (x, y, w, h) = faces[0]
    cropped = img[y:y+h, x:x+w]
    _, buffer = cv2.imencode('.png', cropped)
    base64_img = base64.b64encode(buffer).decode("utf-8")

    return JSONResponse(content={"portrait_base64": base64_img})


@app.post("/extract-portrait/image")
async def extract_portrait_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        raise HTTPException(status_code=404, detail="No face found")

    (x, y, w, h) = faces[0]
    cropped = img[y:y+h, x:x+w]
    _, buffer = cv2.imencode('.png', cropped)

    return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/png")