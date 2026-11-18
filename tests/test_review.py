from app.modules.m7_review.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_review_sample_rows(result):
    assert len(result["final"])==51

def test_review_empty():
    assert ready([],[]) is False

def test_review_control_blocks():
    assert ready([{"status":"CONTROL_FAIL"}],[]) is False

def test_review_negative_allows_manual():
    assert ready([{"status":"NEGATIVE_BLANK"}],[]) is True

def test_review_curve_blocks():
    assert ready([{"status":"PASS"}],[{"status":"CURVE_RANK"}]) is False

def test_review_balance_sample(result):
    assert result["balance"]["input"]==66

def test_review_specific_result(result):
    assert next(r for r in result["final"] if r["sample_id"]=="S002")["concentration"]=="2.0"
