# Deployment Guide for Coding Challenger

This guide outlines the steps to deploy the Coding Challenger application. The project consists of a FastAPI backend and a React (Vite) frontend.

## Prerequisites

- GitHub account
- Accounts on hosting providers (recommendations below)
- Git installed locally

## 1. Backend Deployment (FastAPI)

We recommend using **Render** or **Railway** for the backend as they support Docker natively and have free tiers.

### Option A: Render.com

1.  **Push your code to GitHub**: Ensure your latest changes are committed and pushed.
2.  **Create a New Web Service**:
    - Go to your Render dashboard.
    - Click **New +** -> **Web Service**.
    - Connect your GitHub repository.
3.  **Configure the Service**:
    - **Name**: `coding-challenger-backend` (or similar).
    - **Root Directory**: `backend` (Important: This tells Render where the Dockerfile is).
    - **Environment**: `Docker` (Render should auto-detect this if Root Directory is correct).
    - **Region**: Choose one close to you/your users.
    - **Branch**: `main` (or your working branch).
4.  **Environment Variables**:
    Scroll down to the "Environment Variables" section and add the keys from your `backend/src/.env` file:
    - `OPENAI_API_KEY`: Your OpenAI key.
    - `GROQ_API_KEY`: Your Groq key (if used).
    - `CLERK_SECRET_KEY`: Your Clerk secret key.
    - `CLERK_PUBLISHABLE_KEY`: Your Clerk publishable key.
    - `DATABASE_URL`: Your production database URL.
      > **Note**: For a production database, you might need a managed PostgreSQL instance (Render offers this too). SQLite (`database.db`) will strict work but data will be lost on every redeploy because containers are ephemeral.
5.  **Deploy**: Click **Create Web Service**.

### Option B: Railway.app

1.  **Login to Railway**: Connect with GitHub.
2.  **New Project**: Click **New Project** -> **Deploy from GitHub repo**.
3.  **Select Repo**: Choose your repository.
4.  **Configure**:
    - Railway might try to deploy the root. You need to configure it to deploy the `backend` folder.
    - Go to **Settings** -> **Root Directory** and set it to `/backend`.
5.  **Variables**: Add your environment variables in the **Variables** tab.

## 2. Frontend Deployment (React + Vite)

We recommend **Vercel** or **Netlify** for the frontend.

### Option A: Vercel (Recommended)

1.  **Login to Vercel**: Connect with GitHub.
2.  **Add New Project**: Import your repository.
3.  **Configure Project**:
    - **Framework Preset**: Vite (should be auto-detected).
    - **Root Directory**: Click "Edit" and select `frontend`.
4.  **Build & Output Settings**:
    - Build Command: `npm run build` (default)
    - Output Directory: `dist` (default)
    - Install Command: `npm install` (default)
5.  **Environment Variables**:
    - `VITE_CLERK_PUBLISHABLE_KEY`: Your Clerk Publishable Key.
    - `VITE_API_URL`: The URL of your deployed backend (e.g., `https://coding-challenger-backend.onrender.com`).
      > **Important**: Ensure no trailing slash `/` at the end of the URL if your code appends paths like `/api/...`.
6.  **Deploy**: Click **Deploy**.

### Option B: Netlify

1.  **New Site from Git**: Connect GitHub and choose repo.
2.  **Build Settings**:
    - **Base directory**: `frontend`
    - **Build command**: `npm run build`
    - **Publish directory**: `frontend/dist`
3.  **Environment Variables**: Add them in "Site settings" -> "Environment variables".
4.  **Deploy Site**.

## 3. Post-Deployment Checks

1.  **Verify Backend**: Visit your backend URL (e.g., `https://.../docs`). You should see the Swagger UI.
2.  **Verify Frontend**: Open your deployed frontend app.
3.  **Test Connectivity**:
    - Sign in with Clerk.
    - Try to generate a challenge.
    - Check the browser console (F12) for any CORS errors or 404s if things fail.

## Troubleshooting

-   **CORS Issues**: If the frontend cannot talk to the backend, check `backend/src/app.py` (or main definition) and ensure `CORSMiddleware` includes your deployed frontend domain in `allow_origins`.
    ```python
    # Example in backend/src/app.py
    origins = [
        "http://localhost:5173",
        "https://your-frontend-app.vercel.app" # Add this!
    ]
    ```
-   **Database**: If you use SQLite, remember data persists only as long as the container runs. For persistent data, use a cloud PostgreSQL (Supabase, Neon, Render PostgreSQL).
