from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.routers import email_verifier, rate_limiter

# Initialize FastAPI app
app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(email_verifier.router)
app.include_router(rate_limiter.router)

# Root endpoint to render the HTML page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})