from decimal import Decimal
from app.report import report

def classify(value,lod,overrange=False,control_error=None):
    if overrange:return "OVER_RANGE"
    if control_error is not None and control_error>Decimal("0.20"):return "CONTROL_FAIL"
    if value<0:return "NEGATIVE_BLANK"
    if value<lod:return "BELOW_LOD"
    return "PASS"

def apply(ctx):
    out=[]
    for r in ctx["concentrations"]:
        c=ctx["curves"][(r["batch"],r["analyte"])];x=dict(r)
        error=abs(r["concentration"]-r["level_value"])/r["level_value"] if r["kind"]=="control" and r["level_value"] else None
        x["status"]=classify(r["concentration"],r["lod"],r["response"]>c["max_response"],error)
        x["qualifier"]="<" if x["status"]=="BELOW_LOD" else ""
        out.append(x)
    ctx["quality"]=out
    return report(out,通过=sum(r["status"]=="PASS" for r in out),复核=sum(r["status"]!="PASS" for r in out))
