# Face Extractor API
A simple API that extracts a face/portrait from an uploaded image and returns it as a base64 string.

## Endpoint
- POST `/extract-portrait/` with a form-data image file

## Response
```json
{
  "portrait_base64": "<base64 string>"
}
