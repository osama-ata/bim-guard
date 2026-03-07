import uvicorn

if __name__ == "__main__":
    # Run uvicorn programmatically to avoid stdin closure issues with turbo repo on Windows
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
