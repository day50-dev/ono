"""
Integration tests for Ono.
"""

import pytest
import tempfile
import os
from ono import OnoParser


class TestFormatConversion:
    """Test format conversion functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = OnoParser()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_markdown_conversion(self):
        """Test conversion to markdown."""
        text = "Hello <?ono bold world ?>"
        parsed = self.parser.parse(text)
        markdown = self.parser.to_markdown(parsed)
        assert 'Hello' in markdown

    def test_html_conversion(self):
        """Test conversion to HTML."""
        text = "Hello <?ono emph world ?>"
        parsed = self.parser.parse(text)
        html = self.parser.to_html(parsed)
        assert 'Hello' in html

    def test_text_conversion(self):
        """Test conversion to plain text."""
        text = "Hello <?ono echo world ?>"
        parsed = self.parser.parse(text)
        text_output = self.parser.to_text(parsed)
        assert 'Hello' in text_output

    def test_rst_conversion(self):
        """Test conversion to reStructuredText."""
        text = "Hello <?ono strong world ?>"
        parsed = self.parser.parse(text)
        rst = self.parser.to_rst(parsed)
        assert 'Hello' in rst

    def test_latex_conversion(self):
        """Test conversion to LaTeX."""
        text = "Hello <?ono math E = mc^2 ?>"
        parsed = self.parser.parse(text)
        latex = self.parser.to_latex(parsed)
        assert 'Hello' in latex

    def test_json_conversion(self):
        """Test conversion to JSON."""
        text = "Hello <?ono title Test ?>"
        parsed = self.parser.parse(text)
        json_output = self.parser.to_json(parsed)
        assert 'Hello' in json_output

    def test_xml_conversion(self):
        """Test conversion to XML."""
        text = "Hello <?ono para text ?>"
        parsed = self.parser.parse(text)
        xml = self.parser.to_xml(parsed)
        assert 'Hello' in xml

    def test_yaml_conversion(self):
        """Test conversion to YAML."""
        text = "Hello <?ono list item ?>"
        parsed = self.parser.parse(text)
        yaml = self.parser.to_yaml(parsed)
        assert 'Hello' in yaml


class TestFileProcessing:
    """Test file processing functionality."""

    def test_read_input(self):
        """Test reading input file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ono', delete=False) as f:
            f.write("Hello <?ono echo world ?>")
            f.flush()
            try:
                content = OnoParser.read_input(f.name)
                assert 'Hello' in content
            finally:
                os.unlink(f.name)

    def test_write_output(self):
        """Test writing output file."""
        output_file = os.path.join(self.temp_dir, "output.txt")
        OnoParser.write_output(output_file, "Hello world")
        assert os.path.exists(output_file)
        with open(output_file) as f:
            assert f.read() == "Hello world"
