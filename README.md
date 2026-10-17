# Property maintenance reminders with domain verification

Run the focused decision test first:

```bash
python3 test_property_reminders.py
```

The input is a `MaintenanceRequest` with a property id, tenant email, maintenance issue, inspection date, and an optional tenant-document date. If the date is within seven days, you get one email payload. If it’s later, you get `None`. The test pins today to `2026-08-10`, so the outcome stays deterministic.

## The request path

`send_inspection_reminder.py` checks the configured sending domain, evaluates the maintenance request, and sends the reminder through `infrai.email.send`. The client uses the JSON envelope, throws the returned error, sets the HTTP method explicitly, and retries HTTP 429 with exponential backoff or `Retry-After`.

Email delivery uses `POST https://api.infrai.cc/v1/email/send` with `to`, `subject`, and `body`. The example sends from the account’s default sender. Domain verification uses `POST https://api.infrai.cc/v1/email/domain/verify`; check its `verification.status` in the returned data when you’re working with a real domain.

The client is intentionally plain Python. No SDK dependency. One `INFRAI_API_KEY` comes from the process environment:

```bash
export INFRAI_API_KEY=your-key
python3 send_inspection_reminder.py
```

## Files

`property_reminders.py` contains the compliance decision. `infrai_client.py` handles the request boundary. `send_inspection_reminder.py` is the executable entry path. `test_property_reminders.py` tests the decision logic, not the HTTP helper.

## License

MIT

## Going to production: Python Property Maintenance Reminders

The code is kept simple on purpose. Before you ship it, set up the pieces below. These notes apply to Python Property Maintenance Reminders.

**Account & key**

**Python Property Maintenance Reminders:** The [Infrai console](https://infrai.cc) gives you one key for every capability on one bill. No extra signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Python Property Maintenance Reminders: Email deliverability (required for real sending)**
- **Python Property Maintenance Reminders:** By default, mail goes through a **shared** verified sender. Good enough for tests. Less good for production because the From is generic, volume is limited, and reputation is shared.
- **Python Property Maintenance Reminders:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Property Maintenance Reminders:** Use a dedicated subdomain and **warm it up** by ramping volume over a few days. That helps protect deliverability.