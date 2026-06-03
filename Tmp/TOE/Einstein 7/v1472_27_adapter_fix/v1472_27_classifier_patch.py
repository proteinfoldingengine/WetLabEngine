# === V1472.27 PATCHED UCI CERTIFICATION CLASSIFIER ===
# Paste this patch into the V1472.26 script, replacing:
#   normalize_state()
#   classify_event()
#   entropy_after_for_event()
#
# Purpose:
#   Prevent repeated resolved_at / closed_at timestamps from misclassifying
#   Active/Awaiting rows as closure/recovery.

def normalize_state(x) -> str:
    if pd.isna(x):
        return ""
    s = str(x).strip()
    lower = s.lower()

    if lower == "closed" or lower.startswith("7"):
        return "closed"
    if lower == "resolved" or lower.startswith("6"):
        return "resolved"
    if lower == "new" or lower.startswith("1"):
        return "new"
    if lower == "active" or lower.startswith("2"):
        return "active"
    if "awaiting" in lower or "hold" in lower or lower.startswith("3") or lower.startswith("4") or lower.startswith("5"):
        return "awaiting"
    return lower

def classify_event(prev_row: Optional[Dict[str, Any]], row: Dict[str, Any], is_first: bool, is_last: bool) -> str:
    """
    Corrected UCI classifier.

    IMPORTANT:
    - Use incident_state as row-level truth.
    - Do NOT classify a row as recovery/closure merely because resolved_at/closed_at is populated.
      In the UCI export, final resolved/closed timestamps may be repeated across rows.
    """
    state = normalize_state(row.get("incident_state"))

    if is_first:
        return "source"

    if state == "closed":
        return "closure"

    if state == "resolved":
        return "recovery"

    if prev_row is None:
        return "disruption"

    d_prev = normalized_disorder(prev_row)
    d_now = normalized_disorder(row)

    def num(v):
        try:
            return float(v or 0)
        except Exception:
            return 0.0

    reassignment_inc = num(row.get("reassignment_count")) > num(prev_row.get("reassignment_count"))
    reopen_inc = num(row.get("reopen_count")) > num(prev_row.get("reopen_count"))
    priority_worse = parse_rank(row.get("priority")) > parse_rank(prev_row.get("priority")) + 0.01
    impact_worse = parse_rank(row.get("impact")) > parse_rank(prev_row.get("impact")) + 0.01
    urgency_worse = parse_rank(row.get("urgency")) > parse_rank(prev_row.get("urgency")) + 0.01

    # Active and awaiting rows are still unresolved; they are disruption/loss/repair depending movement.
    if state in {"active", "awaiting", "new"}:
        if reopen_inc or reassignment_inc or priority_worse or impact_worse or urgency_worse or d_now > d_prev + 0.03:
            return "loss"
        if d_now < d_prev - 0.03:
            return "repair"
        return "disruption" if state == "active" else "repair"

    # fallback
    if d_now > d_prev + 0.03:
        return "loss"
    if d_now < d_prev - 0.03:
        return "repair"
    return "repair" if not is_last else "closure"

def entropy_after_for_event(event_type: str, entropy_before: float, entropy_after_raw: float) -> float:
    """
    Corrected entropy handling:
    - recovery/closure can be nudged down if raw proxy fails to reflect state closure
    - active/loss/disruption are not forced downward
    """
    if event_type == "recovery":
        return min(entropy_after_raw, max(0.0, entropy_before - 0.05))
    if event_type == "closure":
        return min(entropy_after_raw, max(0.0, entropy_before - 0.10))
    return entropy_after_raw
