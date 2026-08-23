"""Business rules for inspection reminders and tenant document follow-up."""

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class MaintenanceRequest:
    property_id: str
    tenant_email: str
    issue: str
    inspection_due: date
    document_due: date | None = None


def reminder_for(request, today):
    """Return one action when either compliance date is within seven days."""
    dates = [request.inspection_due]
    if request.document_due is not None:
        dates.append(request.document_due)
    if min(dates) > today + timedelta(days=7):
        return None
    return {
        "to": request.tenant_email,
        "subject": "Property inspection and document reminder",
        "text": (
            "Property " + request.property_id + ": " + request.issue +
            ". Please confirm access and submit any requested tenant documents."
        ),
    }
