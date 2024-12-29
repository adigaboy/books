import uvicorn

def main():
    from app import app
    uvicorn.run(app)

main()