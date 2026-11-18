from app.modules.m3_curve.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_curve_sample(result):
    c=result["reports"][2]["rows"][0];assert Decimal(c["slope"])==2

def test_curve_exact_intercept():
    c=fit([(Decimal(0),Decimal(1)),(Decimal(1),Decimal(3)),(Decimal(2),Decimal(5))]);assert c["intercept"]==1

def test_curve_rank():
    with pytest.raises(BusinessError,match="不独立"):fit([(Decimal(1),Decimal(x)) for x in [2,3,4]])

def test_curve_insufficient():
    with pytest.raises(BusinessError):fit([(Decimal(1),Decimal(2))])

def test_curve_negative_slope():
    with pytest.raises(BusinessError):fit([(Decimal(x),Decimal(3-x)) for x in range(3)])

def test_curve_order_independent():
    p=[(Decimal(x),Decimal(2*x+1)) for x in range(4)];assert fit(p)==fit(p[::-1])

def test_curve_sample_r2(result):
    assert Decimal(result["reports"][2]["rows"][0]["r2"])==1
