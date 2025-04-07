# 🧠 IP Subnet Calculation Knowledge Base

Mathematical logic behind subnetting attributes as implemented in the `ip_subnet_props.py` program.

---

[1. Network Address](#1-network-address)  
[2. Broadcast Address](#2-broadcast-address)  
[3. Subnet Mask ↔ CIDR Conversion](#3-subnet-mask--cidr-conversion)  
[4. Number of Usable Hosts](#4-number-of-usable-hosts)  
[5. First and Last Usable IPs](#5-first-and-last-usable-ips)  
[6. Subnet Group Size](#6-subnet-group-size)  
[7. Next and Previous Network Addresses](#7-next-and-previous-network-addresses)  

---

## 1. Network Address

- **Definition**: The first address in a subnet. Identifies the network; not usable by hosts.
- **Calculation**:
  ```
  network_address = ip & subnet_mask
  ```
  (Bitwise AND between IP address and subnet mask.)

---

## 2. Broadcast Address

- **Definition**: The last address in a subnet. Used to send data to all hosts on the subnet.
- **Calculation**:
  ```
  broadcast_address = network_address | ~subnet_mask
  ```
  (Bitwise OR between network address and inverted subnet mask.)

---

## 3. Subnet Mask ↔ CIDR Conversion

- **CIDR from Subnet Mask**:
  ```
  CIDR = Number of 1s in the binary form of subnet mask
  ```
- **Subnet Mask from CIDR**:
  ```
  subnet_mask = First `CIDR` bits are 1, remaining are 0
  ```
  Example: `/24` → `255.255.255.0`

---

## 4. Number of Usable Hosts

- **Formula**:
  ```
  usable_hosts = 2^(32 - CIDR) - 2
  ```
- **Implementation Note**:
  - The script handles exceptions explicitly:
    - `/31`: Usable hosts = 2 (both addresses are usable — for point-to-point links per RFC 3021)
    - `/32`: Usable hosts = 0 (there are no other addresses available; represents a single endpoint)
- **Clarification**:
  - Even though `/32` represents a valid IP, it doesn't have a usable host range. It's often used for loopback addresses or routing entries targeting one specific host.


## 5. First and Last Usable IPs

- **First Usable IP**:
  ```
  first_usable_ip = network_address + 1
  ```
- **Last Usable IP**:
  ```
  last_usable_ip = broadcast_address - 1
  ```
- **Exceptions**:
  - `/31`: First = Network, Last = Broadcast
  - `/32`: Both = Host IP

---

## 6. Subnet Group Size

- **Formula**:
  ```
  group_size = 2^(32 - CIDR)
  ```
  Total number of IPs in the subnet, including network and broadcast.

---

## 7. Next and Previous Network Addresses

- **Next Network**:
  ```
  next_network = network_address + group_size
  ```
- **Previous Network**:
  ```
  previous_network = network_address - group_size
  ```
  If previous < 0, it's outside the IPv4 range.

---
