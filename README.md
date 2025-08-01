# Face Extractor API

This is a small Python API I built to extract just the face from a passport or ID image. It takes the image, crops the portrait, and returns it as a base64 string.

## How it works
You send a `POST` request to `/extract-portrait/` with the image as form-data (key = `file`). The API processes the image and returns the portrait in base64 format. Simple and easy to integrate into other systems.

## Endpoint
`POST /extract-portrait/`

**Body (form-data):**
- `file`: the image you want to extract the face from

**Response:**
```json
{
  "portrait_base64": "<base64 string>"
}

