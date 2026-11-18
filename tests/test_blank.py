from app.modules.m4_blank.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_blank_sample(result):
    assert len(result["corrected"])==51

def test_blank_negative_preserved():
    assert corrected(Decimal("0.2"),{"intercept":Decimal(1),"slope":Decimal(2)},Decimal("0.1"))==Decimal("-0.5")

def test_blank_zero():
    assert corrected(Decimal(1),{"intercept":Decimal(1),"slope":Decimal(2)},Decimal(0))==0

def test_blank_sample_low(result):
    assert Decimal(next(r for r in result["corrected"] if r["sample_id"]=="S001")["net"])<0

def test_blank_median(result):
    assert len(result["reports"][3]["rows"])==51

def test_blank_missing(sample):
    from app.pipeline import run
    text="\n".join(l for l in sample.splitlines() if ",blank," not in l)
    r=run(text);assert any(x["reason"]=="BLANK_MISSING" for x in r["quarantine"])

def test_blank_curve_missing(sample):
    from app.pipeline import run
    text="\n".join(l for l in sample.splitlines() if ",standard," not in l)
    r=run(text);assert any(x["reason"]=="CURVE_MISSING" for x in r["quarantine"])
