## 1. Cable both networks

The shop (till-1, till-2 and switch **sw-shop**), the back office (accounts, manager and **sw-back**) and one **router** are already on the canvas. In **Design** mode, choose **Cable** and join each computer to its own switch. Then cable the router to **sw-shop first** and to **sw-back** second: the router's first interface, G0/0, then faces the shop and G0/1 faces the back office.

- [ ] Each computer cabled to its own switch
- [ ] Router cabled to sw-shop, then to sw-back
- [ ] The first goal is ticked

> Hint: Each router interface belongs to one network, so each needs its own address. That's why a router joins networks and a switch doesn't.

?> How many router interfaces do you use here? :: 2
