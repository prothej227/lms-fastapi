import uvicorn
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LMS Backend Server")
    parser.add_argument(
        "--host", type=str, default="localhost", help="Host to run the server on."
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to run the server on."
    )
    parser.add_argument(
        "--reload", action="store_true", default=True, help="Enable auto-reload."
    )
    args = parser.parse_args()

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)
