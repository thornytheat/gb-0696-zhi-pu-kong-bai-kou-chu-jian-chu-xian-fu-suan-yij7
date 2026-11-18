from statistics import median
from app.report import report,quarantine
from decimal import Decimal

def corrected(response,curve,blank):
    return (response-curve["intercept"])/curve["slope"]-blank

def apply(ctx):
    blanks={}
    for r in ctx["normalized"]:
        key=(r["batch"],r["analyte"]);c=ctx["curves"].get(key)
        if c and r["kind"]=="blank":blanks.setdefault(key,[]).append((r["response"]-c["intercept"])/c["slope"])
    ctx["blanks"]={k:median(v) for k,v in blanks.items()};out=[]
    for r in ctx["normalized"]:
        if r["kind"] not in {"sample","control"}:continue
        key=(r["batch"],r["analyte"]);curve=ctx["curves"].get(key)
        if not curve:quarantine(ctx,r,"CURVE_MISSING");continue
        if key not in ctx["blanks"]:quarantine(ctx,r,"BLANK_MISSING");continue
        x=dict(r);x["net"]=corrected(r["response"],curve,ctx["blanks"][key]);out.append(x)
    ctx["corrected"]=out
    return report(out,样品=len(out),空白组=len(blanks))
