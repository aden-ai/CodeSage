from pathlib import Path

LANG_MAP = {
    ".py": "Python",
    ".c": "C",
    ".cpp": "C++",
    ".js": "JavaScript",
    ".java": "Java",
    ".ts": "TypeScript",
    ".go": "Go",
    ".rb": "Ruby",
    ".php": "PHP",
}

def detect_language(filename: str, content: str = ""):
    ext = Path(filename).suffix.lower()
    if ext in LANG_MAP:
        return LANG_MAP[ext]

    # fallback simple heuristic
    if "def " in content and "import " in content:
        return "Python"
    if "#include" in content:
        return "C"
    if "console.log(" in content:
        return "JavaScript"
    return "Unknown"
