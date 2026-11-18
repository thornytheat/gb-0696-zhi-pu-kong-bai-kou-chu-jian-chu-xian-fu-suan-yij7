from app.modules.m5_concentration.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_concentration_sample(result):
    assert len(result["concentrations"])==51

def test_concentration_dilution():
    assert concentration(Decimal("0.25"),Decimal(20))==5

def test_concentration_negative():
    assert concentration(Decimal("-0.2"),Decimal(2))==Decimal("-0.4")

def test_concentration_zero_dilution():
    with pytest.raises(ValueError):concentration(Decimal(1),Decimal(0))

def test_concentration_sample_unit(result):
    assert {r["unit"] for r in result["concentrations"]}=={"ug/L"}

def test_concentration_sample_lod(result):
    r=next(r for r in result["concentrations"] if r["sample_id"]=="S002");assert Decimal(r["lod"])==Decimal("0.10")

def test_concentration_no_rounding():
    assert concentration(Decimal("0.333333"),Decimal(3))==Decimal("0.999999")
