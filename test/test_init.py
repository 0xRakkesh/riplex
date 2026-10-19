import importlib.util
from pathlib import Path


def test_main_cli_output(capsys):
    """Test that riplex.__init__.main() executes and outputs greeting."""
    init_path = Path(__file__).parent.parent / "src" / "riplex" / "__init__.py"
    spec = importlib.util.spec_from_file_location("riplex_cli_init", init_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello from riplex!"
