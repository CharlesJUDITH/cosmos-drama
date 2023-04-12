from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
import datetime
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Initialize counters
days_without_issues = 0
days_without_drama = 0

# Prometheus metrics
days_without_issues_counter = Counter("days_without_issues", "Days without issues")
days_without_drama_counter = Counter("days_without_drama", "Days without drama")

class PushDays(BaseModel):
    days: int

# Update the counters every day at midnight
def update_counters():
    global days_without_issues, days_without_drama

    while True:
        now = datetime.datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        time_to_midnight = (midnight - now).seconds
        time.sleep(time_to_midnight)

        days_without_issues += 1
        days_without_issues_counter.inc()

        days_without_drama += 1
        days_without_drama_counter.inc()

# Run the counter update in a separate thread
import threading
counter_thread = threading.Thread(target=update_counters)
counter_thread.start()

@app.get("/", response_class=HTMLResponse)
def read_root():
    global days_without_issues, days_without_drama

    # Generate HTML with the counter values and the image
    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Days without issues and drama</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
            }}
            .counter {{
                font-size: 48px;
                font-weight: bold;
                margin: 20px;
                background-color: #f0f0f0;
                display: inline-block;
                padding: 20px;
                border-radius: 10px;
            }}
            img {{
                max-width: 100%;
                height: auto;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Days without issues and drama in the Cosmos Ecosystem</h1>
        <div class="counter">Days without issues: {days_without_issues}</div>
        <div class="counter">Days without drama: {days_without_drama}</div>
        <img src="https://www.dailydot.com/wp-content/uploads/693/44/f74bf8fba3ce40739c1425f3488cce7c.jpg" alt="Image">
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/push_drama")
def push_drama(payload: PushDays):
    global days_without_drama

    days = payload.days
    if days < 0:
        raise HTTPException(status_code=400, detail="Invalid number of days")

    days_without_drama += days
    days_without_drama_counter.inc(days)
    return {"message": f"Days without drama has been pushed by {days} days"}

@app.post("/push_issues")
def push_issues(payload: PushDays):
    global days_without_issues

    days = payload.days
    if days < 0:
        raise HTTPException(status_code=400, detail="Invalid number of days")

    days_without_issues += days
    days_without_issues_counter.inc(days)
    return {"message": f"Days without issues has been pushed by {days} days"}

@app.get("/metrics")
def metrics():
    return PlainTextResponse(content=generate_latest().decode("utf-8"), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
