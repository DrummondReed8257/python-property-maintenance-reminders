from datetime import date

from property_reminders import MaintenanceRequest, reminder_for


def test_inspection_due_within_seven_days_creates_one_reminder():
    request = MaintenanceRequest(
        property_id="P-42",
        tenant_email="tenant@example.test",
        issue="window latch",
        inspection_due=date(2026, 8, 15),
        document_due=date(2026, 8, 30),
    )
    result = reminder_for(request, date(2026, 8, 10))
    assert result["to"] == "tenant@example.test"
    assert result["subject"] == "Property inspection and document reminder"


def test_later_dates_do_not_send():
    request = MaintenanceRequest("P-42", "tenant@example.test", "window latch", date(2026, 9, 1))
    assert reminder_for(request, date(2026, 8, 10)) is None


if __name__ == "__main__":
    test_inspection_due_within_seven_days_creates_one_reminder()
    test_later_dates_do_not_send()
    print("property reminder tests passed")
