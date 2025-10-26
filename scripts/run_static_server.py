#!/usr/bin/env python3
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402

host = os.getenv("STATIC_HOST", "127.0.0.1")
port = int(os.getenv("STATIC_PORT", "5050"))

app.run(host=host, port=port, debug=False, use_reloader=False)
