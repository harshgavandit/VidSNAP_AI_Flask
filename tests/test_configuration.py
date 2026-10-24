"""Offline configuration checks: no narration/provider request is made."""
from pathlib import Path
import os
import runpy
import unittest
from unittest.mock import patch

CONFIG = Path(__file__).resolve().parents[1] / "config.py"


class ConfigurationTests(unittest.TestCase):
    def test_explicit_environment_value_is_used(self):
        synthetic_key = "sk_test_configuration_only_not_a_real_key"
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": synthetic_key}, clear=True):
            configured = runpy.run_path(str(CONFIG))
        self.assertTrue(configured.get("ELEVENLABS_API_KEY") == synthetic_key,
                        "Configuration must use the supplied environment value")

    def test_missing_key_stops_narration_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "ELEVENLABS_API_KEY"):
                runpy.run_path(str(CONFIG))

    def test_blank_key_is_rejected(self):
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "   "}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "ELEVENLABS_API_KEY"):
                runpy.run_path(str(CONFIG))


if __name__ == "__main__":
    unittest.main()
