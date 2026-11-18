from app.reader import read_rows
from app.report import report,quarantine
FIELDS="sample_id kind analyte area internal_area level dilution unit batch".split()
def apply(ctx):
    rows,bad,blank=read_rows(ctx["text"],FIELDS)
    ctx["quarantine"].extend(bad);ctx["blank_rows"]=blank
    ctx["input_count"]=len(rows)+len(bad)+blank
    kept=[];seen={}
    for r in rows:
        if not r["sample_id"]: quarantine(ctx,r,"ID_REQUIRED");continue
        key=(r["batch"],r["analyte"],r["sample_id"])
        content=tuple(r[k] for k in FIELDS)
        if key in seen:
            quarantine(ctx,r,"DUPLICATE" if seen[key]==content else "KEY_CONFLICT");continue
        seen[key]=content;kept.append(r)
    ctx["raw"]=kept
    return report(kept,采信=len(kept),隔离=len(ctx["quarantine"]),空行=blank)
