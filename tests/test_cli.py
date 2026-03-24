import sys
import pytest
from pathlib import Path
from unittest.mock import patch
from mdpdf.cli import main


def test_cli_no_args_exits_nonzero(capsys):
    with pytest.raises(SystemExit) as exc:
        sys.argv = ["mdpdf"]
        main()
    assert exc.value.code != 0


def test_cli_nonexistent_file_exits_1(tmp_path, capsys):
    missing = tmp_path / "missing.md"
    sys.argv = ["mdpdf", str(missing)]
    with pytest.raises(SystemExit) as exc:
        main()
    captured = capsys.readouterr()
    assert exc.value.code == 1
    assert str(missing) in captured.err and "not found" in captured.err.lower()


def test_cli_calls_convert_and_render(tmp_path):
    md_file = tmp_path / "doc.md"
    md_file.write_text("# Hello")

    with (
        patch("mdpdf.cli.convert", return_value="<h1>Hello</h1>") as mock_convert,
        patch("mdpdf.cli.render_template", return_value="<html></html>") as mock_template,
        patch("mdpdf.cli.render_pdf") as mock_render,
    ):
        sys.argv = ["mdpdf", str(md_file)]
        main()

    mock_convert.assert_called_once_with("# Hello")
    mock_template.assert_called_once_with("<h1>Hello</h1>")
    mock_render.assert_called_once()
    # output path is alongside the source file
    call_args = mock_render.call_args
    output_path: Path = call_args[0][1]
    assert output_path == tmp_path / "doc.pdf"


def test_cli_prints_success_message(tmp_path, capsys):
    md_file = tmp_path / "doc.md"
    md_file.write_text("# Hello")

    with (
        patch("mdpdf.cli.convert", return_value="<h1>Hello</h1>"),
        patch("mdpdf.cli.render_template", return_value="<html></html>"),
        patch("mdpdf.cli.render_pdf"),
    ):
        sys.argv = ["mdpdf", str(md_file)]
        main()

    captured = capsys.readouterr()
    assert "PDF saved:" in captured.out
    assert "doc.pdf" in captured.out


def test_cli_non_md_extension_warns_and_proceeds(tmp_path, capsys):
    txt_file = tmp_path / "doc.txt"
    txt_file.write_text("# Hello")

    with (
        patch("mdpdf.cli.convert", return_value="<h1>Hello</h1>"),
        patch("mdpdf.cli.render_template", return_value="<html></html>"),
        patch("mdpdf.cli.render_pdf"),
    ):
        sys.argv = ["mdpdf", str(txt_file)]
        main()  # should not raise

    captured = capsys.readouterr()
    assert "PDF saved:" in captured.out
    assert "warning" in captured.err.lower() or ".md" in captured.err.lower()
