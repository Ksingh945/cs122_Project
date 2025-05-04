from app import create_app

app = create_app()

print("Running Flask app...")

if __name__ == "__main__":
    app.run(debug=True)
