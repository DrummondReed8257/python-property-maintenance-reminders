"""Runnable example: verify a sending domain, then send a due-date reminder."""

from datetime import date, timedelta

from infrai_client import InfraiClient
from property_reminders import MaintenanceRequest, reminder_for


def main():
    # The same boundary is commonly called infrai.email.send in application code.
    domain = "mail.example-property.test"
    request = MaintenanceRequest(
        property_id="BLDG-17-204",
        tenant_email="chenhua@changba.com",
        issue="leaking kitchen tap",
        inspection_due=date.today() + timedelta(days=3),
        document_due=date.today() + timedelta(days=10),
    )
    client = InfraiClient()
    verification = client.verify_domain(domain)
    print("domain verification:", verification)
    reminder = reminder_for(request, date.today())
    if reminder is None:
        print("no reminder due")
        return
    sent = client.send_email(reminder["to"], reminder["subject"], reminder["text"])
    print("sent message:", sent)


if __name__ == "__main__":
    main()
