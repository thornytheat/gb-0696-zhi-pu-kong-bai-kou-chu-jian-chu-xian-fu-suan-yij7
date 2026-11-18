# TRAP-15
# TRAP-10
# TRAP-07
# TRAP-06
from app.modules.m2_internal.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_internal_sample(result):
    assert len(result["normalized"])==60

def test_internal_fullwidth():
    assert response("１,２００","１００")==Decimal(12)

def test_internal_zero():
    with pytest.raises(BusinessError):response("10","0")

def test_internal_sentinel():
    with pytest.raises(BusinessError):response("N/A","100")

def test_internal_decimal_exact():
    assert response("0.3","0.1")==3

def test_internal_units(result):
    assert all(Decimal(r["level_value"])>=0 for r in result["normalized"])

def test_internal_bad_unit(result):
    assert any(r["reason"]=="UNIT" for r in result["quarantine"])
