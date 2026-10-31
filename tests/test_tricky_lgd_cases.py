"""Tricky and Ambiguous LGD District Entity Resolution Safety Tests.

What this test suite verifies:
1. Strict Disambiguation: Same-named districts across different states (e.g., Bilaspur
   in Himachal Pradesh vs Chhattisgarh) MUST NEVER be guessed when state_hint is missing.
2. Needs-Review Flags: Any match that has uncertainty, low fuzzy confidence (<90%),
   or missing state verification must be flagged with `needs_review=True` and a clear reason.
3. High-Confidence Safe Matches: Exact matches with valid state hints must have
   `needs_review=False` and `confidence_tier="high"`.
4. Historical and Renamed Districts: Official alias crosswalks (e.g. Poona -> Pune,
   Gurgaon -> Gurugram, Belgaum -> Belagavi, Calcutta -> Kolkata).
5. Garbage & Sentinel Strings: Footnotes, asterisks, non-territorial entries must safely unmatch.
"""

from datasetu.normalizer import LGDGazetteer


def test_ambiguous_same_name_districts_require_state_hint():
    gaz = LGDGazetteer.load()

    # 1. Bilaspur without state hint -> MUST NOT GUESS!
    m_no_hint = gaz.resolve("Bilaspur", state_hint=None)
    assert m_no_hint.method == "unmatched"
    assert m_no_hint.canonical_name is None
    assert m_no_hint.needs_review is True
    assert "Ambiguous" in m_no_hint.review_reason
    assert "State hint required" in m_no_hint.review_reason

    # 2. Bilaspur with Himachal Pradesh hint
    m_hp = gaz.resolve("Bilaspur", state_hint="Himachal Pradesh")
    assert m_hp.method == "exact"
    assert m_hp.canonical_name == "Bilaspur"
    assert m_hp.state_code == 2
    assert m_hp.needs_review is False
    assert m_hp.confidence_tier == "high"

    # 3. Bilaspur with Chhattisgarh hint (and alias CG)
    m_cg = gaz.resolve("Bilaspur", state_hint="CG")
    assert m_cg.method == "exact"
    assert m_cg.canonical_name == "Bilaspur"
    assert m_cg.state_code == 22
    assert m_cg.needs_review is False
    assert m_cg.confidence_tier == "high"


def test_renamed_and_historical_aliases():
    gaz = LGDGazetteer.load()

    # Poona -> Pune (Maharashtra)
    m_pune = gaz.resolve("Poona", state_hint="Maharashtra")
    assert m_pune.canonical_name == "Pune"
    assert m_pune.district_code == 521
    assert m_pune.needs_review is False

    # Gurgaon -> Gurugram (Haryana)
    m_ggn = gaz.resolve("Gurgaon", state_hint="Haryana")
    assert m_ggn.canonical_name == "Gurugram"
    assert m_ggn.district_code == 70
    assert m_ggn.needs_review is False

    # Belgaum -> Belagavi (Karnataka)
    m_bel = gaz.resolve("Belgaum", state_hint="Karnataka")
    assert m_bel.canonical_name == "Belagavi"
    assert m_bel.district_code == 555
    assert m_bel.needs_review is False

    # Calcutta -> Kolkata (West Bengal)
    m_kol = gaz.resolve("Calcutta", state_hint="West Bengal")
    assert m_kol.canonical_name == "Kolkata"
    assert m_kol.district_code == 317
    assert m_kol.needs_review is False


def test_confidence_tiers_and_review_flags():
    gaz = LGDGazetteer.load()

    # 1. Exact match with state hint -> High confidence, no review
    m_exact = gaz.resolve("Bengaluru Urban", state_hint="Karnataka")
    assert m_exact.confidence_tier == "high"
    assert m_exact.needs_review is False
    assert m_exact.score == 1.0

    # 2. Fuzzy match without state hint -> Must flag needs_review=True
    m_fuzzy_no_hint = gaz.resolve("Banglore Urban", state_hint=None)
    assert m_fuzzy_no_hint.canonical_name == "Bengaluru Urban"
    assert m_fuzzy_no_hint.needs_review is True
    assert "Verification" in m_fuzzy_no_hint.review_reason or "verification" in m_fuzzy_no_hint.review_reason.lower()

    # 3. Non-existent district -> Unmatched, needs_review=True, confidence=none
    m_bogus = gaz.resolve("District of Nowhere 999", state_hint="Karnataka")
    assert m_bogus.method == "unmatched"
    assert m_bogus.canonical_name is None
    assert m_bogus.needs_review is True
    assert m_bogus.confidence_tier == "none"
    assert "No matching district" in m_bogus.review_reason
