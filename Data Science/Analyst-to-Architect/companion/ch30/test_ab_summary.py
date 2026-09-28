import pytest
from ab_summary import two_proportion_summary


def test_enquiry_form_matches_the_book():
    result = two_proportion_summary(937, 24_036, 1_035, 23_250)
    assert result["diff"] == pytest.approx(0.0055, abs=0.0001)
    assert result["ci_low"] == pytest.approx(0.0019, abs=0.0001)
    assert result["ci_high"] == pytest.approx(0.0091, abs=0.0001)
    assert result["p_value"] == pytest.approx(0.0026, abs=0.0001)
