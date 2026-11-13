## 4. Finding 2: someone else's order

Log in as the demo customer and open one of your orders. The API call is `/api/orders/` and a number. Change the number. If the shop gives you an order that isn't yours, that's an **insecure direct object reference** (IDOR): the API checks that you're logged in, not that the thing is yours.

```tool proxy
{"m": "GET", "p": "/api/orders/2", "h": "Authorization: Bearer {{token}}", "b": "", "s": 200, "blank": ["p", "b"]}
```

- [ ] Log in as demo@nimbu.shop first (Login tab), so `{{token}}` holds your token
- [ ] Your own orders are 3 and 4; ask for 2
- [ ] Note what you saw, then stop: one record proves it
- [ ] The fix: the query must include the caller's user ID

> Hint: Writing down someone's address in a report is itself a data leak. Say "order 2 belongs to another customer; it showed a delivery address", not the address.

?> Which order number belongs to someone else and proves the finding? :: 2
