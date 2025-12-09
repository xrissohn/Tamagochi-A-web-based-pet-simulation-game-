# Tamagochi Game - AI Developer Instructions

## 🎮 Preview Configuration

This project has a **live preview** feature configured.

### Preview Server
- **Port**: 3000
- **URL**: https://3000-i7zmn9tjh57296yt5ojaw-de59bda9.sandbox.novita.ai/index.html
- **Type**: Web Application Preview with Tabbed Interface

### Main Application
- **Port**: 8000
- **URL**: https://8000-i7zmn9tjh57296yt5ojaw-de59bda9.sandbox.novita.ai
- **Type**: Django Web Application

## 🚀 Running Services

Two servers are currently running:

1. **Django Game Server (Port 8000)**
   ```bash
   cd /home/user/webapp && python3 manage.py runserver 0.0.0.0:8000
   ```

2. **Preview Page Server (Port 3000)**
   ```bash
   cd /home/user/webapp && python3 -m http.server 3000
   ```

## 📱 Preview Features

The preview page (`index.html`) includes:
- **Game Preview Tab**: Main game interface
- **Login Tab**: User login page
- **Sign Up Tab**: New user registration
- **Information Tab**: Game features and documentation

## 🔧 Development

- Framework: Django 6.0
- Database: SQLite (development)
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Real-time: Django Channels

## 📝 Important Notes

- X-Frame-Options middleware is disabled to allow iframe embedding
- CSRF protection is configured for the sandbox environment
- Email backend is set to console for development

## 🌐 Preview Tab Activation

To view the preview in AI Developer:
1. Click the "미리보기" (Preview) tab in the top menu
2. Or visit: https://3000-i7zmn9tjh57296yt5ojaw-de59bda9.sandbox.novita.ai/index.html
