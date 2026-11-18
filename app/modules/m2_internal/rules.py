from app.numbers import number,fmt
from app.report import report,quarantine
from app.errors import BusinessError
from decimal import Decimal
UNITS={"ug/L":Decimal(1),"mg/L":Decimal(1000),"ng/L":Decimal("0.001")}
def response(area,internal):
    a,b=number(area),number(internal)
    if a<0 or b<=0: raise BusinessError("INTERNAL","内标须大于零")
    return a/b

def apply(ctx):
    out=[]
    for r in ctx["raw"]:
        try:
            x=dict(r);x["response"]=response(r["area"],r["internal_area"])
            if r["unit"] not in UNITS: raise BusinessError("UNIT","浓度单位无效")
            x["level_value"]=number(r["level"])*UNITS[r["unit"]]
            x["dilution_value"]=number(r["dilution"])
            if x["dilution_value"]<=0: raise BusinessError("DILUTION","稀释倍数须大于零")
            if r["kind"] not in {"standard","blank","sample","control"}: raise BusinessError("KIND","样品类型无效")
            out.append(x)
        except BusinessError as e: quarantine(ctx,r,e.code)
    ctx["normalized"]=out
    return report(out,有效=len(out),单位="响应比")
