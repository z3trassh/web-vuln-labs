# Lab 03: single-use coupon race condition

A coupon may be redeemed once. The endpoint checks that it has not been used,
then marks it used.

## The bug

```python
if coupon["used"]:
    abort(409)
time.sleep(...)        # any real work: a DB write, a payment call
coupon["used"] = True
```

Between the check and the write, other requests run the same check and still see
`used == False`. Many parallel requests each pass the gate once.

## The exploit

`exploit.py` fires the redeem request from many threads at once. The vulnerable
app accepts several; the single coupon is spent more than once.

## The fix

`fixed.py` guards the check-and-set with a lock, so the first request flips the
flag before any other reads it. A database equivalent is a conditional update
(`UPDATE ... WHERE used = false` and inspect the affected-row count) or a unique
constraint on a redemption row.
