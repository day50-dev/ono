"""
Unit tests for the Ono parser.
"""

import pytest
from ono import OnoParser


class TestParserBasic:
    def setup_method(self):
        self.parser = OnoParser()

    def test_parse_simple_text(self):
        result = self.parser.parse("Hello world")
        assert len(result) == 1
        assert result[0].type == 'text'

    def test_parse_ono_block(self):
        result = self.parser.parse('<?ono echo test ?>')
        assert len(result) == 1
        assert result[0].type == 'ono'

    def test_parse_nested_blocks(self):
        result = self.parser.parse('<?ono inner<?ono nested?>?>')
        assert result[0].type == 'ono'
        assert result[0].parsed is not None

    def test_extract_ono_blocks(self):
        text = '<?ono echo 1 ?><?ono echo 2 ?>'
        parsed = self.parser.parse(text)
        blocks = self.parser.extract_ono_blocks(parsed)
        assert len(blocks) == 2

    def test_render_output(self):
        text = 'Hello <?ono echo world ?>'
        parsed = self.parser.parse(text)
        rendered = self.parser.render(parsed)
        assert 'Hello' in rendered


class TestParserEdgeCases:
    def setup_method(self):
        self.parser = OnoParser()

    def test_empty_input(self):
        result = self.parser.parse("")
        assert len(result) == 0

    def test_no_ono_blocks(self):
        result = self.parser.parse("plain text")
        assert result[0].type == 'text'

    def test_unclosed_block(self):
        result = self.parser.parse('<?ono test')
        assert result[0].type == 'text'


class TestParserNesting:
    def setup_method(self):
        self.parser = OnoParser()

    def test_deep_nesting(self):
        text = '<?ono a<?ono b<?ono c?>?>?>'
        result = self.parser.parse(text)
        assert result[0].type == 'ono'

    def test_multiple_siblings(self):
        text = '<?ono a?><?ono b?><?ono c?>'
        result = self.parser.parse(text)
        assert len(result) == 3

    def test_mixed_content(self):
        text = 'before<?ono inner?>after'
        result = self.parser.parse(text)
        assert result[0].type == 'text'
        assert result[1].type == 'ono'
        assert result[2].type == 'text'
