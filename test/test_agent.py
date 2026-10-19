from unittest.mock import patch, MagicMock
from riplex.services.agent import run_agent, llm, agent


def test_agent_and_llm_configuration():
    """Verify LLM and agent attributes are properly configured."""
    assert llm.model_name == "qwen/qwen3.8-27b"
    assert llm.temperature == 0.7
    assert agent is not None


def test_run_agent_success():
    """Verify run_agent invokes agent and extracts the last message content."""
    mock_msg1 = MagicMock()
    mock_msg1.content = "What is reinforcement learning?"
    mock_msg2 = MagicMock()
    mock_msg2.content = "Reinforcement learning is a branch of machine learning."

    mock_result = {
        "messages": [mock_msg1, mock_msg2]
    }

    with patch.object(agent, "invoke", return_value=mock_result) as mock_invoke:
        answer = run_agent("What is reinforcement learning?")

        mock_invoke.assert_called_once_with({
            "messages": [{"role": "user", "content": "What is reinforcement learning?"}]
        })
        assert answer == "Reinforcement learning is a branch of machine learning."


def test_run_agent_single_response_message():
    """Verify run_agent handles a single returned message properly."""
    mock_msg = MagicMock()
    mock_msg.content = "Simple answer."
    mock_result = {"messages": [mock_msg]}

    with patch.object(agent, "invoke", return_value=mock_result):
        answer = run_agent("Quick question")
        assert answer == "Simple answer."
