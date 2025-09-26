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
```app/
├─ api/ # API endpoints (auth, chat, file upload)
├─ models/ # Database models (User, Chat, File)
├─ schemas/ # Request/response validation with Pydantic
├─ services/ # Business logic (chat flow, file parsing)
├─ repositories/# Database CRUD operations
├─ core/ # Config, security, and app settings
└─ main.py # FastAPI application entry point
```

---

## 🌐 Technology Stack
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (Azure Database for PostgreSQL recommended)
- **Storage:** Azure Blob Storage for file uploads (planned)
- **Auth:** Microsoft Entra ID for OAuth2 / OpenID Connect (planned)
- **AI Integration:** Azure OpenAI / RAG for medical insights (future)

---

## ☁️ Azure Deployment Overview
This project is built to be deployed on **Microsoft Azure** for scalability and security.  
Here’s a high-level roadmap for deployment:

### 1️⃣ Create Azure Resources
- **Resource Group** – Central container for all project resources.  
- **Azure Database for PostgreSQL** – Create a flexible server and obtain the connection string.  
- **Azure Storage Account** – Enable Blob Storage for file uploads.  
- **Microsoft Entra ID (Azure AD)** – Register an app for authentication and get Tenant ID, Client ID, and Secret.  
- *(Optional)* **Azure Application Insights** – For logging and performance monitoring.

### 2️⃣ Configure Environment Variables
Set environment variables or an `.env` file with:
```DATABASE_URL=...
BLOB_CONNECTION_STRING=...
AZURE_TENANT_ID=...
AZURE_CLIENT_ID=...
AZURE_CLIENT_SECRET=...
```

Use Azure Key Vault for production secrets.

### 3️⃣ Deploy the FastAPI App
- **Option A:** Azure App Service  
  - Push your code to a GitHub repo.  
  - Create a Web App in Azure App Service and enable GitHub Actions for CI/CD.  
- **Option B:** Azure Container Apps  
  - Build a Docker image and deploy via Azure Container Registry.  
  - Scale based on traffic automatically.

### 4️⃣ Enable Monitoring & Scaling
- Connect Application Insights to track performance and API logs.
- Set auto-scaling rules in App Service or Container Apps for cost optimization.

---

## 📊 Future Roadmap
- 🤖 **Intelligent AI Support** – Connect to Azure OpenAI for medical result interpretation and guidance.
- 🧩 **Role-Based Access Control** – Doctor/patient-specific permissions and data privacy.
- 📈 **Advanced Analytics** – User behavior tracking and report generation.

---

## 💡 Vision
This backend aims to become the foundation of a secure, AI-assisted healthcare platform,  
where patients can share reports, consult doctors, and receive intelligent medical feedback — all in one place.
