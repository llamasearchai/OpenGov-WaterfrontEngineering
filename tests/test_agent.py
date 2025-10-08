"""
Tests for OpenAI agent integration.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from open_gov_waterfront.agent import WaterfrontAgent


def test_agent_initialization_with_key() -> None:
    """Test agent initialization with provided API key."""
    with patch("open_gov_waterfront.agent.OpenAI") as mock_openai:
        agent = WaterfrontAgent(api_key="test_key", model="gpt-4")
        assert agent.api_key == "test_key"
        assert agent.model == "gpt-4"
        mock_openai.assert_called_once_with(api_key="test_key")


def test_agent_initialization_with_env_key() -> None:
    """Test agent initialization using environment variable."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "env_key"}):
        with patch("open_gov_waterfront.agent.OpenAI") as mock_openai:
            agent = WaterfrontAgent()
            assert agent.api_key == "env_key"
            assert agent.model == "gpt-4o-mini"
            mock_openai.assert_called_once_with(api_key="env_key")


def test_agent_initialization_without_key() -> None:
    """Test agent initialization fails without API key."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="OpenAI API key required"):
            WaterfrontAgent()


def test_agent_query() -> None:
    """Test agent query method."""
    with patch("open_gov_waterfront.agent.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        agent = WaterfrontAgent(api_key="test_key")
        response = agent.query("Test question")

        assert response == "Test response"
        mock_client.chat.completions.create.assert_called_once()


def test_agent_query_with_context() -> None:
    """Test agent query with context."""
    with patch("open_gov_waterfront.agent.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Contextual response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        agent = WaterfrontAgent(api_key="test_key")
        context = {"project": "Ferry Terminal", "location": "SF Bay"}
        response = agent.query("What conditions?", context=context)

        assert response == "Contextual response"
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        assert len(messages) == 2
        assert "Context:" in messages[1]["content"]


def test_agent_suggest_calculation() -> None:
    """Test agent suggest_calculation method."""
    with patch("open_gov_waterfront.agent.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Suggested calculations"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        agent = WaterfrontAgent(api_key="test_key")
        result = agent.suggest_calculation("New wharf project")

        assert result == {"suggestion": "Suggested calculations"}
        mock_client.chat.completions.create.assert_called_once()


def test_agent_interpret_results() -> None:
    """Test agent interpret_results method."""
    with patch("open_gov_waterfront.agent.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Results interpretation"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        agent = WaterfrontAgent(api_key="test_key")
        inputs = {"mass_tonnes": 8000, "speed_knots": 0.5}
        results = {"energy_J": 264653, "fender_reaction_kN": 756}
        interpretation = agent.interpret_results("berthing", inputs, results)

        assert interpretation == "Results interpretation"
        mock_client.chat.completions.create.assert_called_once()
