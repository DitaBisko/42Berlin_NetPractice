# IP Subnet Properties Checker

This project was something I built as part of the **NetPractice** module from the **42 Network curriculum** — but honestly, it was mainly for me.

I created this tool because I wanted to understand networking and subnetting **deeply**, not just memorize formulas or blindly use online calculators. Writing the logic myself — calculating network and broadcast addresses, host ranges, and CIDR math — helped me learn how it *actually works*. I also used it to get better at **Python**, so it became a small personal sandbox.

---
* [🧠  I built this tool to:](#-i-built-this-tool-to)
* [🛠️ What It does](#-what-it-does)
* [📁 Files](#-files)
* [▶️ How to use](#-how-to-use)
* [🧪 Running the Tests](#-running-the-tests)

---
## 🧠  I built this tool to:

- Double-check my manual calculations
- Break subnetting down step-by-step in code
- Use `ipaddress` from Python's standard library as a **self-check**
- Learn how to test and validate logic with integration tests

---

## 🛠️ What It does

- Takes an IP address and subnet (CIDR or mask)
- Calculates:
  - Network address
  - Broadcast address
  - First and last usable IPs
  - Number of usable hosts
  - Subnet mask / CIDR conversions
- Detects special/reserved ranges using `reserved_ip.json`
  - Private
  - Loopback
  - Link-local
  - Multicast
  - Reserved
- Integration test compares custom logic to Python's `ipaddress` module for validation

---

## 📁 Files

- `ip_subnet_props.py` – main script that calculates everything
- `integration_test_ip_subnet_props.py` – test runner for checking logic vs Python’s standard `ipaddress` module
- `reserved_ip.json` – definitions and metadata about known reserved IP ranges

---

## ▶️ How to use

Run it from terminal with either CIDR or netmask syntax:

```bash
# Using CIDR
python3 ip_subnet_props.py 192.168.1.45/24

# Or using subnet mask
python3 ip_subnet_props.py 192.168.1.45 255.255.255.0
```

_Output:_
```txt
----- IP Attributes -----

Network address: 192.168.1.0
Broadcast address: 192.168.1.255
Subnet mask: 255.255.255.0
CIDR: /24
Number of usable hosts: 254
First usable IP: 192.168.1.1
Last usable IP: 192.168.1.254
Subnet group size: 256
Next network address: 192.168.2.0
Previous network address: 192.168.0.0

---------- FYI ----------
Category: Private IP address
Usage  : This private range is commonly used in home networks, small
         business networks, and routers as the default IP range (e.g.,
         192.168.1.1 is often a router's gateway address).
```
## 🧪 Running the Tests

To make sure the subnet logic is correct, I wrote integration tests that compare my outputs to Python’s built-in `ipaddress` module.

Run the full test suite with:

```bash
python3 integration_test_ip_subnet_props.py
```

✅ **The tests check:**

- Output formatting and values (e.g. usable hosts, broadcast address)
- Edge cases like `/31`, `/32`, and unusual CIDRs
- Reserved IP categories (e.g. Private, Loopback)
- Input validation and error handling

The output will show which tests passed, which failed, and any mismatches.

