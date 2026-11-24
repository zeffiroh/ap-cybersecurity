## 3. Ping across, then break a gateway

Press **Simulation**, click till-1 and open **Command line**. Ping accounts at 192.168.2.21: the replies say **TTL=127**. Now open the **Data exchange** tab, choose **accounts** in the list, and click an ICMP echo request. Its **Time to live** is 127, one less than the 128 till-1 sent, because the router counted the hop. Its source MAC isn't till-1's either: the router put its own on.

Then press **Design**, clear manager's **Default gateway**, and press **Simulation**. From manager, ping accounts (192.168.2.21, same network): it answers. Ping till-1 (192.168.1.11): **General failure**. Put the gateway back.

- [ ] till-1 to accounts works
- [ ] TTL 127 read in accounts' data exchange
- [ ] Without a gateway, manager only reaches its own network

> Hint: A missing gateway is one of the most common faults on real help desks: "I can print but I can't reach the internet".

?> Without a gateway, can manager reach till-1? (yes or no) :: no

?> What Time to live does till-1's echo request carry when it reaches accounts? :: 127
