from app import create_app

# Create application instance for production
app = create_app()

if __name__ == "__main__":
    app.run()