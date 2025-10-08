"""
Tests for server __main__ execution.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from unittest.mock import patch


def test_server_main_block() -> None:
    """Test server __main__ block execution."""
    with patch("uvicorn.run") as mock_run:
        import runpy

        runpy.run_module("open_gov_waterfront.server", run_name="__main__")
        mock_run.assert_called_once()
