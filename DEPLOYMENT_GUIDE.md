# 🚀 How to Deploy GymTrack Pro Online (Free & Live in 3 Minutes)

Because your database is already hosted on the cloud (**MongoDB Atlas**), your website will instantly be connected to real data once deployed!

---

## Recommended Free Host: **Render.com** (Best for Flask + MongoDB Atlas)

Render provides free hosting with automatic HTTPS (SSL) and continuous deployment.

### Step 1: Push Project to GitHub

1. Open your terminal in this project folder (`coll project`):
   ```bash
   git init
   git add .
   git commit -m "Initial commit of GymTrack Pro"
   ```

2. Go to [GitHub.com](https://github.com), click **New Repository**, name it `gymtrack-pro`, and make it **Public** or **Private**.

3. Push your code to GitHub (replace `<YOUR_GITHUB_USERNAME>` with your GitHub username):
   ```bash
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/gymtrack-pro.git
   git push -u origin main
   ```

---

### Step 2: Deploy on Render (Free)

1. Go to [render.com](https://dashboard.render.com/) and sign up / log in with your **GitHub** account.
2. Click the **"New +"** button in the top bar and select **"Web Service"**.
3. Select your `gymtrack-pro` repository from the list.
4. Fill in these settings:
   - **Name:** `gymtrack-pro` (or any name you like)
   - **Region:** Singapore / Frankfurt / Oregon (any is fine)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** `Free`

5. Scroll down to **"Environment Variables"** and click **"Add Environment Variable"**:
   - **Key:** `MONGO_URI`
   - **Value:** `mongodb+srv://harshlade23_db_user:tx17qur2lgi6eWGB@cluster0.nbhfyy4.mongodb.net/`
   
   *(Optional)* Add a second variable:
   - **Key:** `SECRET_KEY`
   - **Value:** `gymtrack_pro_secret_key_2026`

6. Click **"Create Web Service"** (or **"Deploy Web Service"**).

---

### Step 3: That's It! 🎉

- Render will automatically build the app, install dependencies from `requirements.txt`, and start the Gunicorn server.
- Within **1 to 2 minutes**, you will get a live public URL at the top of your dashboard:
  👉 **`https://gymtrack-pro-xxxx.onrender.com`**
- You can open this link from any mobile phone, laptop, or share it with your professor/evaluator for live demonstration!

---

## Important MongoDB Atlas Network Whitelist Note:
To ensure Render can connect to your MongoDB Atlas cluster:
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/).
2. Click **Network Access** in the left sidebar.
3. Make sure `0.0.0.0/0` (Allow access from anywhere) is listed and active. *(You already configured this during database setup, but good to verify!)*
