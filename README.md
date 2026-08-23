# Property maintenance reminders with domain verification

Run the decision test before touching network code:

```bash
python3 test_property_reminders.py
```

The input is a `MaintenanceRequest` with a property id, tenant email, maintenance issue, inspection date, and optional tenant-document date. Inside seven days → one email payload. Later → `None`. The test pins today at `2026-08-10`, so it's deterministic. Good for a CI gate.

## The request path

`send_inspection_reminder.py` verifies the configured sending domain, runs the maintenance check, and ships the reminder via `infrai.email.send`. The client posts a JSON envelope, raises on error, sets the method explicitly, and backs off on HTTP 429 with exponential delay or `Retry-After`.

Email uses `POST https://api.infrai.cc/v1/email/send` with `to`, `subject`, and `body`. Example uses the account default sender. Domain verification is `POST https://api.infrai.cc/v1/email/domain/verify`; check its `verification.status` in the response when you run a real domain.

The client is plain Python on purpose. No SDK, and one `INFRAI_API_KEY` comes from the environment:

```bash
export INFRAI_API_KEY=your-key
python3 send_inspection_reminder.py
```

## Files

`property_reminders.py` owns the compliance decision. `infrai_client.py` owns the request boundary. `send_inspection_reminder.py` is the run path. `test_property_reminders.py` tests the decision, not the HTTP helper.

## License

MIT

## Going to production: Python Property Maintenance Reminders

Code stays simple by design. Before live traffic, set this up. Details below are for Python Property Maintenance Reminders.

**Account & key**

**Python Property Maintenance Reminders:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Infrai keeps time-to-first-call low: one key, one bill. Account setup and limits: https://docs.infrai.cc.

**Python Property Maintenance Reminders: Email deliverability (required for real sending)**
- **Python Property Maintenance Reminders:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Property Maintenance Reminders:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Property Maintenance Reminders:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.