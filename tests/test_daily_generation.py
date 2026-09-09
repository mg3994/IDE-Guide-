import os
import subprocess
import pytest

def test_daily_generation_script():
    cmd = ["python3", "scripts/generate_daily_content.py"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Daily generation completed!" in result.stdout
