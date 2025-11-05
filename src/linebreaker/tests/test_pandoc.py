"""Tests for pandoc integration to ensure linebreaking preserves semantic content."""

import pytest
import subprocess
import tempfile
import os
import re
from pathlib import Path

# Add parent directory to path to allow importing linebreaker
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from linebreaker import break_text


class TestPandocIntegration:
    """Test linebreaking with pandoc conversion to ensure semantic preservation."""

    @staticmethod
    def strip_html_tags(text):
        """Strip HTML tags and normalize whitespace."""
        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def test_comprehensive_linebreaking_with_pandoc_html(self):
        """Test that linebreaking preserves content when converted to HTML via pandoc."""
        # Read the test document
        test_doc_path = Path(__file__).parent / "test_doc.qmd"
        with open(test_doc_path, "r") as f:
            markdown_content = f.read()

        # Check if pandoc is available
        try:
            subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("pandoc not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Write original markdown
            original_md = os.path.join(tmpdir, "original.md")
            with open(original_md, "w") as f:
                f.write(markdown_content)

            # Convert to HTML
            original_html = os.path.join(tmpdir, "original.html")
            subprocess.run(
                [
                    "pandoc",
                    "-f",
                    "markdown",
                    "-t",
                    "html",
                    original_md,
                    "-o",
                    original_html,
                ],
                check=True,
            )

            # Apply linebreaking
            linebroken_md_content = break_text(markdown_content)

            # Write linebroken markdown
            linebroken_md = os.path.join(tmpdir, "linebroken.md")
            with open(linebroken_md, "w") as f:
                f.write(linebroken_md_content)

            # Convert linebroken to HTML
            linebroken_html = os.path.join(tmpdir, "linebroken.html")
            subprocess.run(
                [
                    "pandoc",
                    "-f",
                    "markdown",
                    "-t",
                    "html",
                    linebroken_md,
                    "-o",
                    linebroken_html,
                ],
                check=True,
            )

            # Read and compare HTML content
            with open(original_html, "r") as f:
                original_html_content = f.read()
            with open(linebroken_html, "r") as f:
                linebroken_html_content = f.read()

            # Strip tags and normalize
            original_text = self.strip_html_tags(original_html_content)
            linebroken_text = self.strip_html_tags(linebroken_html_content)

            # Assert they are the same (ignoring HTML formatting differences)
            assert (
                original_text == linebroken_text
            ), f"Text mismatch:\nOriginal: {original_text}\nLinebroken: {linebroken_text}"
