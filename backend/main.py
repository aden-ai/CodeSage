from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# Note: Assuming these imports work and the paths are correct (e.g., in a package)
from backend.openrouter_client import OpenRouterClient
from backend.language_detector import detect_language
from backend.analyzers import run_static_checks
import tempfile, os

app = FastAPI(title="Code Reviewer")

# --- 1. CONFIGURATION ---

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenRouterClient()

# --- 2. STATIC FILE ROUTES (Best Practice) ---

# 1. Define the explicit root route to serve the main HTML file.
# This ensures a GET request to http://127.0.0.1:8000/ works
@app.get("/", response_class=FileResponse)
async def serve_index():
    # Make sure your main HTML file is named index.html inside the frontend folder
    return "frontend/index.html"

# 2. Mount StaticFiles to a separate, non-conflicting path (/static).
# All other assets (JS, CSS, images) should be loaded from /static/
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# --- 3. API ENDPOINT ---

# ✅ This is the single, correct definition for the POST /review API endpoint
@app.post("/review")
async def review_code(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file uploaded"}

    # Use a temporary file to save and process the uploaded file
    # Note: Using tempfile.NamedTemporaryFile is safer than shutil.copyfileobj/os.remove
    tmp_path = ""
    try:
        # Create a temporary file and write the uploaded content
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        code = open(tmp_path).read()
        lang = detect_language(file.filename, code)
        static = run_static_checks(tmp_path, lang)
        llm_output = client.chat(code, lang)

        return {
            "language": lang,
            "summary": llm_output.get("summary"),
            "errors": llm_output.get("errors"),
            "suggestions": llm_output.get("suggestions"),
            "static": static,
        }
    finally:
        # Ensure the temporary file is deleted even if an error occurs
        if os.path.exists(tmp_path):
            os.remove(tmp_path)