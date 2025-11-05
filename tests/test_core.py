"""Tests for line_breaker module."""

import pytest
import sys
import os

# Add parent directory to path to allow importing linebreaker
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linebreaker import (
    mask_citations_and_numbers,
    restore_masked_content,
    split_on_sentence_punctuation,
    split_on_colons,
    split_on_em_dashes,
    format_line,
    break_text,
)


class TestMaskingFunctions:
    """Test citation and number masking."""

    def test_mask_citations(self):
        text = "Some text [@citation1] and more [@citation2]."
        masked, cit_map, num_map = mask_citations_and_numbers(text)

        assert "__CITATION_0__" in masked
        assert "__CITATION_1__" in masked
        assert "[@citation1]" not in masked
        assert len(cit_map) == 2
        assert len(num_map) == 0

    def test_mask_numbers(self):
        text = "AUC 0.85 and 0.28-0.89 values"
        masked, cit_map, num_map = mask_citations_and_numbers(text)

        assert "__N_0__" in masked
        assert "__N_1__" in masked
        assert "__N_2__" in masked
        assert "0.85" not in masked
        assert len(num_map) == 3
        assert len(cit_map) == 0

    def test_mask_both(self):
        text = "Value 0.85 [@doi:link] and 3.14 [@other]"
        masked, cit_map, num_map = mask_citations_and_numbers(text)

        assert len(cit_map) == 2
        assert len(num_map) == 2
        assert "[@" not in masked
        assert "0.85" not in masked

    def test_restore_content(self):
        text = "__CITATION_0__ with __N_0__"
        cit_map = {"__CITATION_0__": "[@citation]"}
        num_map = {"__N_0__": "0.85"}

        restored = restore_masked_content(text, cit_map, num_map)
        assert restored == "[@citation] with 0.85"


class TestSentenceSplitting:
    """Test sentence-level splitting."""

    def test_no_split_short_text(self):
        text = "Short text."
        result = split_on_sentence_punctuation(text)
        assert len(result) == 1

    def test_split_on_period(self):
        text = "This is a sentence with enough characters before the period. And another sentence with sufficient length."
        result = split_on_sentence_punctuation(text)
        assert len(result) == 2

    def test_no_split_on_abbreviation_vs(self):
        text = "This is a comparison of method A vs. method B with more text."
        result = split_on_sentence_punctuation(text)
        # Should NOT split on "vs."
        assert len(result) == 1

    def test_no_split_on_dr(self):
        text = "Dr. Smith conducted the research with sufficient characters here."
        result = split_on_sentence_punctuation(text)
        # Should NOT split on "Dr."
        assert len(result) == 1

    def test_split_on_question_mark(self):
        text = "This is a question with enough characters before it? And this is the answer with enough text."
        result = split_on_sentence_punctuation(text)
        assert len(result) == 2

    def test_no_split_on_et_al(self):
        text = "This research was conducted by Smith et al. and continued with more experiments."
        result = split_on_sentence_punctuation(text)
        # Should NOT split on "et al."
        assert len(result) == 1

    def test_no_split_on_prof(self):
        text = "The study was led by Prof. Johnson who has extensive experience in this field."
        result = split_on_sentence_punctuation(text)
        # Should NOT split on "Prof."
        assert len(result) == 1


class TestColonSplitting:
    """Test colon/semicolon splitting."""

    def test_no_split_short_text(self):
        text = "Short text: with colon"
        result = split_on_colons(text, min_length=80)
        assert len(result) == 1

    def test_split_long_text_with_colon(self):
        text = "This is a very long sentence with more than eighty characters here: and this is the continuation part."
        result = split_on_colons(text, min_length=80)
        assert len(result) == 2
        assert result[0].endswith(":")

    def test_no_split_if_parts_too_short(self):
        text = "This is text: short continuation that doesn't meet the minimum"
        result = split_on_colons(text, min_length=80)
        # Won't split if parts are < 20 chars
        assert len(result) == 1


class TestFormatLine:
    """Test the complete line formatting."""

    def test_simple_sentence(self):
        line = "This is a simple sentence."
        result = format_line(line)
        assert result == line

    def test_multiple_sentences(self):
        line = "First sentence with enough characters for proper detection. Second sentence also has enough characters. Third sentence completes it."
        result = format_line(line)
        # Should split into 3 lines
        assert result.count("\n") == 2

    def test_with_citations(self):
        line = "Text with citations [@https://doi.org/10.1038/example]. More text here with sufficient length."
        result = format_line(line)
        # Citation should be preserved
        assert "[@https://doi.org/10.1038/example]" in result

    def test_with_decimal_numbers(self):
        line = "The value was 0.85 in the first test. The second test showed 0.92 as the result."
        result = format_line(line)
        # Numbers should be preserved
        assert "0.85" in result
        assert "0.92" in result

    def test_long_sentence_with_colon(self):
        line = "However, fecal-based approaches show highly inconsistent performance for adenoma detection: a systematic review of microbiome-derived biomarkers found diagnostic values."
        result = format_line(line)
        # Should split at colon since sentence is >80 chars
        lines = result.split("\n")
        assert len(lines) >= 2
        assert lines[0].endswith(":")

    def test_no_split_on_vs(self):
        line = "This is a comparison study of treatment A vs. treatment B showing significant results with enough text."
        result = format_line(line)
        # Should NOT split on "vs."
        assert result.count("\n") == 0 or "vs.\n" not in result

    def test_complex_real_world_example(self):
        line = "The _gut_ microbiome has been shown to be strongly altered in CRC, with fecal metagenomes predictive of established CRC (AUC 0.85) [@https://doi.org/10.1038/s41591-025-03693-9]. However, fecal-based approaches show highly inconsistent performance for adenoma detection: a systematic review of microbiome-derived biomarkers (mostly 16S rDNA sequencing) found diagnostic AUCs ranging from 0.28-0.89 with high variability across studies [@https://doi.org/10.1016/j.neo.2022.100868]."
        result = format_line(line)

        # Should preserve all citations
        assert "[@https://doi.org/10.1038/s41591-025-03693-9]" in result
        assert "[@https://doi.org/10.1016/j.neo.2022.100868]" in result

        # Should preserve all numbers
        assert "0.85" in result
        assert "0.28" in result
        assert "0.89" in result

        # Should split into multiple lines
        assert "\n" in result

    def test_em_dash_goes_to_new_line(self):
        line = "The gut microbiome has been shown to be strongly altered in CRC — with fecal metagenomes predictive of established CRC values."
        result = format_line(line)
        # Em dash should start the new line
        assert "\n—" in result or result.startswith("—")
        # Should NOT have em dash at end of first line
        assert "—\n" not in result

    def test_colon_stays_on_first_line(self):
        line = "However, fecal-based approaches show highly inconsistent performance: a systematic review found diagnostic values."
        result = format_line(line)
        # Colon should end the first line
        lines = result.split("\n")
        if len(lines) > 1:
            assert lines[0].endswith(":")

    def test_parentheses_end_breaking_very_long(self):
        line = "This is a very long sentence with some information in parentheses (like this information here that makes it longer) and then more text continues after the parentheses for quite a while to make it over one hundred characters."
        result = format_line(line)
        # Should break after closing parenthesis in very long sentences
        assert "\n" in result

    def test_enumeration_parentheses_no_break(self):
        line = "They rely exclusively on 16S rRNA amplicon sequencing, which: (1) provides only genus- or species-level resolution, (2) systematically misses Patescibacteria—the most prevalent phylum in the oral cavity, and (3) cannot resolve subspecies-level variation known to be functionally critical."
        result = format_line(line)
        # Should NOT break after enumeration markers like (1), (2), (3)
        assert "(1)\n" not in result
        assert "(2)\n" not in result
        assert "(3)\n" not in result
        # Should break on commas instead
        assert "," in result
        assert "\n" in result


class TestEmDashSplitting:
    """Test em dash splitting."""

    def test_em_dash_breaks_to_new_line(self):
        text = "This is a very long sentence with more than enough characters here — and this is the continuation after the em dash."
        result = split_on_em_dashes(text, min_length=80)
        assert len(result) == 2
        # Em dash should start the second part
        assert result[1].startswith("—")

    def test_no_split_short_text_with_em_dash(self):
        text = "Short text — with em dash"
        result = split_on_em_dashes(text, min_length=80)
        assert len(result) == 1


class TestQuartoBlocks:
    """Test handling of Quarto ::: blocks."""

    def test_quarto_triple_colon_block(self):
        text = """---
title: Test
---

This is a normal line that should be formatted if long enough to trigger breaks.

::: {.callout-note}
This is inside a Quarto block: it should not be formatted at all even if very long.
:::

This is another normal line that should be formatted."""
        result = break_text(text)
        # Content inside ::: block should be preserved
        assert "::: {.callout-note}" in result
        assert ":::" in result
        # Check that the block content is preserved
        lines = result.split("\n")
        assert any("This is inside a Quarto block" in line for line in lines)

    def test_quarto_quadruple_colon_block(self):
        text = """---
title: Test
---

Normal text here.

:::: {.columns}
Content inside four-colon block: should not be formatted.
::::

More normal text."""
        result = break_text(text)
        # Content inside :::: block should be preserved
        assert ":::: {.columns}" in result
        assert "::::" in result.split("\n")[-2] or "::::" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
