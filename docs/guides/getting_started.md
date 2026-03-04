# Getting Started

## 1. Frontend Setup (Next.js)

```bash
npm install
npm run dev
```

## 2. Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```
