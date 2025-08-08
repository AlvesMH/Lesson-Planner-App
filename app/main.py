# File: app/main.py
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"  # LangChain
os.environ["POSTHOG_DISABLED"] = "true"       # Gradio & LC fallback

import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

from .ui import app

if __name__ == "__main__":
    import tempfile, pathlib
    app().launch(
        allowed_paths=[
            str(pathlib.Path.cwd()),          # project dir
            tempfile.gettempdir(),            # Gradio’s upload temp
        ],
        favicon_path=None                     # stops 404 /manifest.json
    )