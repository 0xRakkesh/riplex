import importlib
import os
from unittest.mock import patch


def test_config_loads_environment_variables():
    """Verify that config loads API keys and LangSmith settings."""
    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "test-tavily-key",
            "GROQ_API_KEY": "test-groq-key",
            "LANGSMITH_TRACING": "true",
            "LANGSMITH_API_KEY": "test-langsmith-key",
        },
        clear=False,
    ):
        import riplex.core.config as config
        importlib.reload(config)

        assert config.TAVILY_API_KEY == "test-tavily-key"
        assert config.GROQ_API_KEY == "test-groq-key"
        assert config.LANGSMITH_TRACING == "true"
        assert config.LANGSMITH_API_KEY == "test-langsmith-key"


def test_config_with_missing_environment_variables():
    """Verify config behavior when environment variables are not set."""
    with patch.dict(os.environ, {}, clear=True):
        import riplex.core.config as config
        importlib.reload(config)

        assert config.TAVILY_API_KEY is None or isinstance(config.TAVILY_API_KEY, str)
        assert config.GROQ_API_KEY is None or isinstance(config.GROQ_API_KEY, str)
