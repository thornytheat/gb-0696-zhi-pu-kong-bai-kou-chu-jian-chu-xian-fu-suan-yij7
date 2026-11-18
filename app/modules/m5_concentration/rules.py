from app.numbers import fmt
from app.report import report
from decimal import Decimal

def concentration(net,dilution):
    if dilution<=0:raise ValueError("稀释倍数须为正")
    return net*dilution

def apply(ctx):
    out=[]
    for r in ctx["corrected"]:
        x=dict(r);x["concentration"]=concentration(r["net"],r["dilution_value"]);x["lod"]=Decimal("0.05")*r["dilution_value"];x["unit"]="ug/L";out.append(x)
    ctx["concentrations"]=out
    return report(out,复算=len(out),单位="ug/L")
