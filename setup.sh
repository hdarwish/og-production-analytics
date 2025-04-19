#!/bin/bash

# Create virtual environment for backend
echo "Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

# Create frontend directory and install dependencies
echo "Setting up frontend..."
cd frontend
npm install
cd ..

echo "Setup complete!"
echo "To run the backend server:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run: uvicorn backend.app.main:app --reload"
echo ""
echo "To run the frontend:"
echo "1. Open a new terminal"
echo "2. cd frontend"
echo "3. Run: ng serve"
echo ""
echo "Access the application at http://localhost:4200" 