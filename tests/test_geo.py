# tests/test_geo.py

from hamcrest import assert_that, is_
from geo import is_valid_us_zip


def test_zip_not_digits():
    assert_that(is_valid_us_zip("abcde"), is_(False))
    assert_that(is_valid_us_zip("123a5"), is_(False))


def test_zip_has_spaces():
    assert_that(is_valid_us_zip("90 210"), is_(False))


def test_zip_is_empty_string():
    assert_that(is_valid_us_zip(""), is_(False))


def test_zip_too_short():
    assert_that(is_valid_us_zip("123"), is_(False))


def test_zip_too_long():
    assert_that(is_valid_us_zip("123456"), is_(False))


def test_zip_plus_4_not_supported():
    assert_that(is_valid_us_zip("20500+1600"), is_(False))
    assert_that(is_valid_us_zip("20500-1600"), is_(False))


def test_zip_just_right():
    assert_that(is_valid_us_zip("12345"), is_(True))
    assert_that(is_valid_us_zip("90210"), is_(True))
    assert_that(is_valid_us_zip("00000"), is_(True))
