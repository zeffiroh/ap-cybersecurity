## 2. Write the access list

On the router:

```
configure terminal
access-list 120 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
access-list 120 permit tcp 192.168.20.0 0.0.0.255 any eq 80
access-list 120 permit udp 192.168.20.0 0.0.0.255 any eq 53
access-list 120 deny ip any any
interface g0/0.20
 ip access-group 120 in
end
show access-lists
```

Rules are read top to bottom and the first match wins, so the deny for the staff network comes first.

- [ ] Access list 120 written in the right order
- [ ] Applied inbound on the guest subinterface
- [ ] show access-lists checked

> Hint: A wildcard mask is the opposite of a netmask: 0.0.0.255 means "any value in the last number".

?> Which wildcard mask matches a whole /24 network? :: 0.0.0.255

?> Which interface gets the list, inbound? (as typed in the command) :: g0/0.20
