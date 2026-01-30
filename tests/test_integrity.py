import unittest
import os
from pathlib import Path
import sys
import urllib.request
import json

# Agregar root al path para importar scripts
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(REPO_ROOT))

class TestFrameworkIntegrity(unittest.TestCase):

    def test_directory_structure(self):
        """Verifica que existan los directorios críticos."""
        required_dirs = [".context", "agents", "skills", "workspaces", "sessions", "scripts", "docs"]
        for d in required_dirs:
            self.assertTrue((REPO_ROOT / d).exists(), f"Directory missing: {d}")

    def test_master_context(self):
        """Verifica que MASTER.md exista."""
        master = REPO_ROOT / ".context" / "MASTER.md"
        self.assertTrue(master.exists())

    def test_scripts_presence(self):
        """Verifica que los scripts críticos existan."""
        scripts = ["pa.py", "sync-context.py", "install.py", "server.py", "stats_etl.py"]
        for s in scripts:
            self.assertTrue((REPO_ROOT / "scripts" / s).exists(), f"Script missing: {s}")

    def test_dashboard_assets(self):
        """Verifica que los logos y librerías offline existan."""
        assets = ["docs/lib/logo-horizontal.png", "docs/lib/tailwind.js", "docs/lib/alpine.min.js"]
        for a in assets:
            self.assertTrue((REPO_ROOT / a).exists(), f"Asset missing: {a}")

    def test_api_status(self):
        """Verifica que la API de status responda (si el servidor está corriendo)."""
        try:
            with urllib.request.urlopen("http://localhost:8085/api/status", timeout=2) as response:
                data = json.loads(response.read().decode())
                self.assertIn("version", data)
                self.assertEqual(data["orchestration"], "active")
        except urllib.error.URLError:
            self.skipTest("Server is not running on http://localhost:8085")

if __name__ == '__main__':
    unittest.main()