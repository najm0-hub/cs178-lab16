# CS 178 — Lab 15: Serverless Image Processing

Starter repo for Lab 15. See the lab instructions on HackMD for setup steps.

## Files
| File | Role | Who writes it |
|---|---|---|
| `app.py` | Flask web server | You fill in the boto3 upload (Exercise 1) |
| `templates/index.html` | Upload form + result display | Pre-built |
| `lambda_function.py` | Lambda: flips the image | Pre-built — read and understand it |
| `lambda_function_rekognition.py` | Lambda: flip + Rekognition labels | You fill in the Rekognition call (Stretch) |
| `requirements.txt` | Python dependencies for Flask app | Pre-built |

## Running locally
```bash
pip install -r requirements.txt
python app.py
```
Then open http://localhost:5000
