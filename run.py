from src.optimized import app
import os

if __name__ == "__main__":
    app.run("0.0.0.0", port=os.getenv('PORT', 8800))
