import subprocess

def run_static_checks(file_path: str, language: str):
    """
    Runs basic static analysis or syntax checks depending on the language.
    Returns a summary of issues or 'No issues detected'.
    """

    try:
        if language.lower() == "python":
            # Run flake8 or pyflakes for Python
            result = subprocess.run(["python", "-m", "py_compile", file_path],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                return f"Python Syntax Error:\n{result.stderr}"
            else:
                return "✅ No syntax issues detected in Python code."

        elif language.lower() == "c":
            # Check syntax using gcc
            result = subprocess.run(["gcc", "-fsyntax-only", file_path],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                return f"C Compilation Issues:\n{result.stderr}"
            else:
                return "✅ No syntax issues detected in C code."

        elif language.lower() == "cpp":
            # Check syntax using g++
            result = subprocess.run(["g++", "-fsyntax-only", file_path],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                return f"C++ Compilation Issues:\n{result.stderr}"
            else:
                return "✅ No syntax issues detected in C++ code."

        elif language.lower() == "javascript":
            # JS lint via Node
            result = subprocess.run(["node", "--check", file_path],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                return f"JavaScript Syntax Issues:\n{result.stderr}"
            else:
                return "✅ No syntax issues detected in JavaScript code."

        else:
            return f"Static analysis not supported for language: {language}"

    except Exception as e:
        return f"⚠️ Static analysis failed: {str(e)}"
