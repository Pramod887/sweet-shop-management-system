from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .auth.router import router as auth_router
from .sweets.router import router as sweets_router
from .inventory.router import router as inventory_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sweet Shop Management System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(sweets_router, prefix="/api/sweets", tags=["sweets"])
app.include_router(inventory_router, prefix="/api/sweets", tags=["inventory"])


@app.get("/")
def root():
    return {"message": "Sweet Shop Management System API"}

