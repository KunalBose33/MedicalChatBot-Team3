# 🩺 Medical Assistant Chatbot

A **FastAPI-powered backend** for a smart medical chatbot enabling  
patients, doctors, and AI to communicate and share medical data securely.

This backend is designed with scalability and Azure cloud integration in mind,  
serving as the core for a future web application with intelligent health insights.

---

## ✨ Key Features
- **Multi-Role Chat System**  
  Separate channels for doctor–patient communication and AI-assisted guidance.
  
- **Medical File Handling**  
  Secure upload and parsing of CSV and PDF medical reports for analysis.

- **Cloud-Ready Authentication**  
  Architecture supports Microsoft Entra ID (Azure AD) for enterprise-grade identity management.

- **Scalable Architecture**  
  Modular design with clear separation of API routes, services, repositories, and database models.

---

## 🏗️ Project Structure Overview
'''app/
├─ api/ # API endpoints (auth, chat, file upload)
├─ models/ # Database models (User, Chat, File)
├─ schemas/ # Request/response validation with Pydantic
├─ services/ # Business logic (chat flow, file parsing)
├─ repositories/# Database CRUD operations
├─ core/ # Config, security, and app settings
└─ main.py # FastAPI application entry point'''
