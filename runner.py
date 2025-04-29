# runner.py
import subprocess
import multiprocessing
import uvicorn
import os

def run_fastapi():
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000)

def run_streamlit():
    subprocess.run([
        "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.headless", "true"
    ])

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_fastapi)
    p2 = multiprocessing.Process(target=run_streamlit)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
