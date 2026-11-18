from decimal import Decimal
from app.errors import BusinessError
from app.report import report

def fit(points):
    if len(points)<3: raise BusinessError("CURVE_POINTS","至少3个标曲点")
    n=Decimal(len(points));sx=sum(x for x,y in points);sy=sum(y for x,y in points)
    den=n*sum(x*x for x,y in points)-sx*sx
    if den==0: raise BusinessError("CURVE_RANK","标曲浓度不独立")
    slope=(n*sum(x*y for x,y in points)-sx*sy)/den
    if slope<=0: raise BusinessError("CURVE_SLOPE","标曲斜率无效")
    intercept=(sy-slope*sx)/n
    residual=sum((y-(slope*x+intercept))**2 for x,y in points)
    total=sum((y-sy/n)**2 for x,y in points)
    return {"slope":slope,"intercept":intercept,"r2":Decimal(1)-residual/total if total else Decimal(0),"max_response":max(y for x,y in points)}

def apply(ctx):
    groups={};curves={};errors=[]
    for r in ctx["normalized"]:
        if r["kind"]=="standard":groups.setdefault((r["batch"],r["analyte"]),[]).append((r["level_value"],r["response"]))
    for key,points in groups.items():
        try:curves[key]=fit(points)
        except BusinessError as e:errors.append({"batch":key[0],"analyte":key[1],"status":e.code})
    ctx["curves"]=curves;ctx["curve_errors"]=errors
    return report([dict(batch=k[0],analyte=k[1],**v) for k,v in curves.items()]+errors,标曲=len(curves),失败=len(errors))
