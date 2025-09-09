# How to start

1. Start tunnel with ngrok
```
ngrok http 8000
```
2. Start main app
```
uvicorn main:app --reload --port 8000
```
If you want to start it with `python3 main.py` In your `./main.py` file you must have this:
```
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```
