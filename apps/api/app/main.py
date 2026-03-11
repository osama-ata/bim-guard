from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import analyze, rules

app = FastAPI(
    title="BIM Guard API",
    description="Backend API for BIM Guard, powered by ifcopenshell",
    version="1.0.0"
)

# Configure CORS
# In production, this should be restricted to the actual frontend URL
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "BIM Guard API is working", "status": "ok"}

# Include routers
app.include_router(analyze.router, prefix="/api/v1/analyze", tags=["Analyze"])
app.include_router(rules.router, prefix="/api/v1/rules", tags=["Rules"])
