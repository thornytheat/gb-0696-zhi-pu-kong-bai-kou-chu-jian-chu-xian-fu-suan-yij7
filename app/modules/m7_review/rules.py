from app.report import report

def ready(rows,errors):
    return bool(rows) and not errors and not any(r["status"] in {"OVER_RANGE","CONTROL_FAIL"} for r in rows)

def apply(ctx):
    ctx["final"]=ctx["quality"];ctx["blocked"]=not ready(ctx["final"],ctx["curve_errors"])
    excluded={r["line"] for r in ctx["quarantine"]}
    accepted=ctx["input_count"]-len(excluded)-ctx["blank_rows"]
    ctx["balance"]={"input":ctx["input_count"],"accepted":accepted,"quarantined":len(excluded),"blank":ctx["blank_rows"]}
    return report(ctx["final"],结论="阻断" if ctx["blocked"] else "可复核",样品=len(ctx["final"]),隔离=len(excluded))
