from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.rentals import router as rentals_router
from routers.auth import router as auth_router

app = FastAPI(
    title="FlyRent API",
    description="Backend FastAPI per FlyRent con Autenticazione JWT - Smart Working Rental Tracker",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(rentals_router)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "FlyRent FastAPI Backend with Auth"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
