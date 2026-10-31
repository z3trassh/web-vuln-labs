# Lab 04: invoice BOLA (broken object-level authorization)

Each user can read their own invoices at `/invoices/<id>`. A token identifies the
caller.

## The bug

The route checks that the caller is logged in, then returns the invoice for the
requested id. It never checks that the invoice belongs to the caller:

```python
user = authenticate(token)        # who are you
invoice = INVOICES[invoice_id]    # what you asked for — not whose it is
return invoice
```

The id is a sequential integer, so a logged-in user reads everyone's invoices by
changing the number.

## The exploit

`exploit.py` logs in as a normal user, reads its own invoice, then walks nearby
ids and collects the ones that are not its own.

## The fix

`fixed.py` adds one ownership check: the invoice's `owner` must equal the
authenticated user, otherwise 404. It returns 404 rather than 403 so the
response does not reveal that the id exists.
