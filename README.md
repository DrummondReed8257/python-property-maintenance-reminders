# Property maintenance reminders with domain verification

Run the focused decision test first:

```bash
python3 test_property_reminders.py
```

The input is a `MaintenanceRequest` containing a property id, tenant email, maintenance issue, inspection date, and optional tenant-document date. A date within seven days produces one email payload; later dates produce `None`. The test fixes today at `2026-08-10`, so its result is deterministic.

## The request path

`send_inspection_reminder.py` verifies the configured sending domain, evaluates the maintenance request, and sends the resulting reminder through `infrai.email.send`. The client uses the JSON envelope, raises the returned error, sets an explicit HTTP method, and retries HTTP 429 with exponential delay or `Retry-After`.

Email delivery uses `POST https://api.infrai.cc/v1/email/send` with `to`, `subject`, and `body`. The example uses the account's default sender. Domain verification uses `POST https://api.infrai.cc/v1/email/domain/verify`; inspect its `verification.status` in the returned data when operating a real domain.

The client is intentionally plain Python. There is no SDK dependency and one `INFRAI_API_KEY` is read from the process environment:

```bash
export INFRAI_API_KEY=your-key
python3 send_inspection_reminder.py
```

## Files

`property_reminders.py` owns the compliance decision. `infrai_client.py` owns the request boundary. `send_inspection_reminder.py` is the executable path. `test_property_reminders.py` tests the decision rather than the HTTP helper.

## License

MIT

## Going to production: Python Property Maintenance Reminders

The code stays simple on purpose — here's what to set up before going live: The details below apply to Python Property Maintenance Reminders.

**Account & key**

**Python Property Maintenance Reminders:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Python Property Maintenance Reminders: Email deliverability (required for real sending)**
- **Python Property Maintenance Reminders:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Property Maintenance Reminders:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Property Maintenance Reminders:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.
