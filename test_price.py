from .almost_scrapper import parse_price

def test_price_number_returns_number():
    result = parse_price(1234)
    assert result == 1234

def test_string_with_comma():
    result = parse_price("12,34")
    assert result == 1234

def test_string_with_comma_and_real():
    result = parse_price("R$12,34")
    assert result == 1234

def test_string_with_comma_and_real_with_space():
    result = parse_price("R$ 12,34")
    assert result == 1234

def test_empty_string():
    result = parse_price("")
    assert result == 0

def test_big_number():
    result = parse_price("R$ 1.234,55")
    assert result == 123455