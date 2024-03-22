#!/bin/bash

# Start the backend server (FastAPI)
echo "Starting backend server..."
cd backend/src
uvicorn main:app --host 0.0.0.0 --port 7000 &

# Start the frontend server (ReactJS)
echo "Starting frontend server..."
cd ../../frontend/
npm run dev &
