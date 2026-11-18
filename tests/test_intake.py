# TRAP-14
# TRAP-05
# TRAP-01
from app.modules.m1_intake.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_intake_sample_rows(result):
    assert len(result["raw"])==62

def test_intake_encoding(sample):
    from app.reader import decode
    assert decode(sample.encode("gb18030"))==sample

def test_intake_column_isolation(sample):
    from app.pipeline import run
    r=run(sample+"bad,row\n");assert any(x["reason"]=="COLUMN_COUNT" for x in r["quarantine"])

def test_intake_conflicting_key(sample):
    from app.pipeline import run
    r=run(sample+"S001,sample,Pb,600,100,0,1,ug/L,B01\n");assert any(x["reason"]=="KEY_CONFLICT" for x in r["quarantine"])

def test_intake_empty_rejected():
    with pytest.raises(BusinessError,match="文件为空"):read_rows("",FIELDS)

def test_intake_header_only():
    with pytest.raises(BusinessError,match="只有表头"):read_rows(",".join(FIELDS)+"\n",FIELDS)

def test_intake_balance(result):
    assert result["balance"]["quarantined"]>=4

def test_same_sample_id_different_analytes_kept(sample):
    from app.pipeline import run
    extra='\n'.join(line.replace(',Pb,',',As,') for line in sample.splitlines()[1:] if ',Pb,' in line)
    r=run(sample+'\n'+extra+'\n')
    assert {x['analyte'] for x in r['normalized']}=={'Pb','As'}
    assert len(r['final'])==102
