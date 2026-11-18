# TRAP-19
from app.modules.m6_quality.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_quality_sample_negative(result):
    assert next(r for r in result["quality"] if r["sample_id"]=="S001")["status"]=="NEGATIVE_BLANK"

def test_quality_lod_equality():
    assert classify(Decimal("0.05"),Decimal("0.05"))=="PASS"

def test_quality_below_lod():
    assert classify(Decimal("0.04"),Decimal("0.05"))=="BELOW_LOD"

def test_quality_priority():
    assert classify(Decimal(-1),Decimal(1),True,Decimal(1))=="OVER_RANGE"

def test_quality_control_boundary():
    assert classify(Decimal(2),Decimal(1),False,Decimal("0.20"))=="PASS"

def test_quality_control_fail():
    assert classify(Decimal(2),Decimal(1),False,Decimal("0.201"))=="CONTROL_FAIL"

def test_quality_sample_count(result):
    assert len(result["quality"])==51
