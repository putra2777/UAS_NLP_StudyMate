from src.utils import parse_score, route_after_validation, validate_input


def test_parse_score_valid() -> None:
    assert parse_score("SCORE: 87\nKEKUATAN:\n- jelas") == 87


def test_parse_score_clamped() -> None:
    assert parse_score("SCORE: 130") == 100


def test_parse_score_missing() -> None:
    assert parse_score("Tidak ada skor") == 0


def test_short_input_is_invalid() -> None:
    state = {"source_text": "terlalu pendek"}
    result = validate_input(state)
    assert result["error"]
    assert route_after_validation(result) == "invalid"


def test_long_input_is_valid() -> None:
    state = {"source_text": "x" * 150}
    result = validate_input(state)
    assert result["error"] == ""
    assert route_after_validation(result) == "valid"
