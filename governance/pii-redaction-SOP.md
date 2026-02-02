# PII Redaction SOP
**Goal:** Prevent accidental exposure of personal data in SEO deliverables.

1. **Never include** raw query strings, user IDs, IPs, or full URLs with tokens.
2. **Use placeholders**: https://www.example.gov/SECTION/PATH?param=REDACTED
3. **Export hygiene**: Remove row-level IDs before sharing.
4. **Screenshots**: Blur IDs, hide email addresses, remove cookies/toolbars.
5. **Peer check**: A second reviewer validates the redactions before publish/commit.
