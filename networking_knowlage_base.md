# Networking

---

* **[1. Networking fundamentals](#1-networking-fundamentals)**
  * [The OSI model](#-the-osi-model)
    * [The seven layers of the OSI model](#-the-seven-layers-of-the-osi-model)
    * [Data flow in the OSI model](#-data-flow-in-the-osi-model)
  * [The TCP/IP model](#-the-tcpip-model)
    * [The four layers of the TCP/IP model](#-the-four-layers-of-the-tcpip-model)
    * [Data flow in the TCP/IP Model](#-data-flow-in-the-tcpip-model)
  * [LANs, WANs, and network devices](#-lans-wans-and-network-devices)
    * [Local Area Network (LAN)](#-local-area-network-lan)
    * [Wide Area Network (WAN)](#-wide-area-network-wan)
  * [**Key devices in networking**](#-key-devices-in-networking)
    * [**Routers**](#-routers)
    * [**Switches**](#-switches)
    * [**Hubs (Legacy Device)**](#-hubs-legacy-device)
    * [**Access Points (APs)**](#-access-points-aps-)
  * [**How network devices interconnect**](#-how-network-devices-interconnect)
* [**2. IP addressing and subnetting**](#2-ip-addressing-and-subnetting)
  * [**IP address**](#-ip-address)
    * [**IPv4 addressing**](#-ipv4-addressing)
    * [**IPv4 Address Structure**](#-ipv4-address-structure)
    * [**IPv4 Address Classes**](#-ipv4-address-classes-)
  * [**Subnet Masks & CIDR**](#-subnet-masks--cidr)
    * [**CIDR notation**](#-cidr-notation)
  * [**Calculating Subnets**](#-calculating-subnets)
* **[3. Routing and Network Configuration](#3-routing-and-network-configuration)**
  * [Routing Fundamentals](#-routing-fundamentals)
    * [How routers determine the best path](#-how-routers-determine-the-best-path)
    * [Static vs. Dynamic Routing](#-static-vs-dynamic-routing)
      * [Static Routing](#-static-routing)
      * [Dynamic Routing](#-dynamic-routing)
  * [NetPractice focus – Network Elements – Explained Simply](#-netpractice-focus--network-elements--explained-simply)
* **[4. Troubleshooting (logs in NetPractice)](#4-troubleshooting-logs-in-netpractice)**
  * [NetPractice Log Messages – Full Reference](#-netpractice-log-messages--full-reference)
  * [Successful routing & flow](#-successful-routing--flow)
  * [Configuration warnings & intermediate issues](#-configuration-warnings--intermediate-issues)
  * [Failures & errors](#-failures--errors)
  * [Tip for debugging](#-tip-for-debugging)
* **[Glossary](#-glossary)**


---
## 1. Networking fundamentals
Networking is the process of connecting devices—such as computers, servers, and routers—to communicate and share data.  
Networks range from small setups like home Wi-Fi to vast systems like the Internet, 
which connects billions of devices worldwide.  

As networks grow in size and complexity, managing communication efficiently becomes challenging. 
Different devices, operating systems, and technologies need a structured way to interact. 
Without a standard approach, devices would struggle to communicate, leading to inefficiencies and incompatibilities.

To solve this complexity, networking follows a structured set of rules and guidelines. 
These rules ensure that data moves smoothly from one device to another, regardless of hardware or software differences.
This structured approach is defined using **networking models**.

Networking models help standardize communication between devices, ensuring that data is transmitted efficiently and reliably.
The two main models used in networking are the **OSI model** and the **TCP/IP model**.
---
### 💡 The OSI model
The **Open Systems Interconnection (OSI) model** is a conceptual framework that standardizes how devices communicate over a network. 
It divides network communication into seven layers, each responsible for a specific function. 
This layered approach ensures that different technologies and systems can work together seamlessly.

The OSI model provides **standardization**, ensuring that hardware and software from different vendors can communicate effectively. 
Its **troubleshooting** capabilities help isolate and identify network issues by pinpointing the affected layer. 
The modular design of the model assigns distinct roles to each layer, **simplifying network management and development**.

#### 🚀 The seven layers of the OSI model
The OSI model is structured into seven layers, each handling a specific aspect of network communication. 
The layers are ordered from Physical (hardware) to Application (user-facing services).

| Layer               | Function                                  | Example Protocols/Technologies |
|---------------------|-------------------------------------------|--------------------------------|
| **7. Application**  | Provides services to end-users            | HTTP, FTP, SMTP                |
| **6. Presentation** | Translates, encrypts, compresses data     | SSL/TLS, JPEG, ASCII           |
| **5. Session**      | Manages sessions between applications     | NetBIOS, RPC                   |
| **4. Transport**    | Ensures reliable or fast data transfer    | TCP, UDP                       |
| **3. Network**      | Routes data across networks               | IP, ICMP                       |
| **2. Data Link**    | Handles direct node-to-node communication | Ethernet, MAC addresses        |
| **1. Physical**     | Transfers raw bits over physical media    | Cables, Wi-Fi, fiber optics    |

#### 🚀 Data flow in the OSI model
Data moves down through each layer when sent and up when received. Each layer adds a header 
during encapsulation on the sender's side and removes it during decapsulation on the receiver's side.  

_**Example of data transmission using the OSI model**_
- A user sends an email (Application Layer).  
- The email is encrypted and formatted (Presentation Layer).  
- A session is created between sender and receiver (Session Layer).  
- The message is broken into packets (Transport Layer).  
- The packets are addressed and routed (Network Layer).  
- Packets are turned into frames and transmitted (Data Link Layer).  
- The frames are converted into electrical or wireless signals and sent (Physical Layer).  

_At the receiving end, this process reverses, ensuring that the original email is correctly reconstructed and displayed._

---
### 💡 The TCP/IP model

The **Transmission Control Protocol/Internet Protocol (TCP/IP) model** is a practical framework that defines how data is transmitted across networks, including the Internet. 
It was designed to ensure seamless communication between different devices and systems by organizing network functions into four layers. 
Unlike the OSI model, which is more theoretical, the TCP/IP model is directly implemented in real-world networks and serves as the foundation of modern Internet communication.

The TCP/IP model provides scalability, allowing networks to grow without major changes to the overall structure. 
It also ensures interoperability, enabling different devices and technologies to communicate efficiently. 
With its streamlined four-layer design, the model prioritizes real-world implementation over strict separation of responsibilities, making it more adaptable for modern networking needs.

#### 🚀 The four layers of the TCP/IP model
The TCP/IP model simplifies network communication into four layers, with each handling a specific set of tasks. 
These layers map closely to the OSI model but merge certain functionalities for a more practical approach.

| Layer              | Function                                  | Example Protocols/Technologies |
|--------------------|-------------------------------------------|--------------------------------|
| **4. Application** | Provides network services to applications | HTTP, FTP, SMTP, DNS           |
| **3. Transport**   | Manages end-to-end communication          | TCP, UDP                       |
| **2. Internet**    | Handles addressing and routing of packets | IP, ICMP, ARP                  |
| **1. Link**        | Manages physical transmission and framing | Ethernet, Wi-Fi, MAC addresses |

#### 🚀 Data flow in the TCP/IP Model
Data moves down the layers when being sent and up the layers when received. 
Like the OSI model, TCP/IP follows encapsulation (adding headers) during transmission and decapsulation (removing headers) upon reception.


**_Example of data transmission using the TCP/IP model_**
- A user visits a website (Application Layer – HTTP request).
- The request is broken into segments (Transport Layer – TCP or UDP).
- Segments are assigned an IP address and routed (Internet Layer – IP).
- The data is converted into frames and transmitted over the physical medium (Link Layer – Ethernet/Wi-Fi).

_At the receiving end, the data moves back up the layers, reconstructing the original request until the webpage is displayed._

---
### 💡 LANs, WANs, and network devices
Networks come in different sizes and serve different purposes.
The two primary types of networks are **Local Area Networks (LANs) and Wide Area Networks (WANs).** 
Each serves a specific role in connecting devices and enabling communication.

---

#### 🚀 Local Area Network (LAN)
A Local Area Network (LAN) is a network that connects devices within a limited geographical area, such as a home, office, school, or data center.
LANs enable fast and efficient communication between devices and typically use wired (Ethernet) or wireless (Wi-Fi) connections.

**Characteristics of a LAN**  
- Covers a small geographic area (e.g., a building, campus, or office).
- Offers high-speed communication (typically 100 Mbps to 10 Gbps).
- Uses Ethernet cables, Wi-Fi, or fiber optics.
- Managed by a single organization or entity (e.g., a business, school).
- Provides access to shared resources like printers, file servers, and applications.

**_Example of a LAN setup_**  
A company office network where all computers, printers, and servers are connected via Ethernet and Wi-Fi. 
Employees can share files, print documents, and access internal applications without using the Internet.

---

#### 🚀 Wide Area Network (WAN)
A Wide Area Network (WAN) is a network that spans a large geographical area, often connecting multiple LANs across cities, countries, or even globally.
WANs use a combination of public and private networks, including the Internet, leased lines, and satellite links, to provide communication over long distances.

**Characteristics of a WAN**  
- Covers a large geographic area (e.g., multiple offices across cities or countries).
- Uses slower connections compared to LANs (ranging from Mbps to Gbps, depending on the infrastructure).
- Typically relies on public networks (e.g., the Internet) or leased lines from ISPs.
- Managed by multiple organizations or service providers.
- More complex to maintain due to security, cost, and performance concerns.

**_Example of a WAN setup_**  
A multinational corporation with offices in different countries connects its branch networks using a Virtual Private Network (VPN) over the Internet or dedicated leased lines from an ISP.

---

### **💡 Key devices in networking**
To enable communication between devices, networks use specialized hardware. The most common network devices include routers, switches, hubs, and access points.

#### **🚀 Routers**
A router is a device that directs network traffic between different networks.
It determines the best path for data to travel and is essential for connecting LANs to the Internet.

**Functions of a router**
- Routes data between different networks (e.g., between a home network and the Internet).
- Assigns IP addresses using DHCP (Dynamic Host Configuration Protocol).
- Provides security through firewalls and NAT (Network Address Translation).
- Manages network traffic with Quality of Service (QoS).

_**Example**_  
Home router connects Wi-Fi devices to the Internet while managing network traffic between them.

#### **🚀 Switches**
A switch is a network device that connects multiple devices within a LAN.
Unlike a hub, a switch directs data to the correct device rather than broadcasting it to all connected devices.

**Functions of a switch**
- Forwards data only to the intended recipient, improving network efficiency.
- Operates at Layer 2 (Data Link Layer) of the OSI model, using MAC addresses.
- Reduces network congestion by allowing multiple simultaneous data transfers.

_**Example**_  
In an office, a switch connects all computers, printers, and servers to a single network, enabling communication between them.

#### **🚀 Hubs (Legacy Device)**
A hub is an older networking device that connects multiple devices in a LAN but lacks the intelligence of a switch.
Instead of directing data to a specific device, a hub broadcasts data to all connected devices, making it inefficient and outdated.

**Functions of a hub**
- Operates at Layer 1 (Physical Layer) of the OSI model.
- Broadcasts data to all devices, causing network congestion.
- Replaced by switches in modern networks for better efficiency.

**_Example_**  
An early LAN setup where a hub connected multiple computers, leading to excessive network collisions.

#### **🚀 Access Points (APs)**  

A Wireless Access Point (WAP) extends a wired network by enabling Wi-Fi connectivity.
It allows wireless devices to connect to a network without using physical cables.

**Functions of an Access Point**
- Converts wired Ethernet to wireless signals (Wi-Fi).
- Expands the coverage of a network by acting as a relay.
- Can be standalone or part of a larger network (managed APs in enterprises).

**_Example_**
A Wi-Fi router in a home contains a built-in access point, enabling wireless devices to connect to the Internet.

### **💡 How network devices interconnect**
Network devices are interconnected using network topologies, which define how devices communicate. 
The most common topologies include –

| Topology | Description                                                | Advantages                                              | Disadvantages                                           |
|----------|------------------------------------------------------------|---------------------------------------------------------|---------------------------------------------------------|
| **Star** | Devices connect to a central switch/router.                | Easy to manage, scalable, fast performance.             | Single point of failure (if switch/router fails).       |
| **Bus**  | All devices share a single communication line.             | Simple and cost-effective.                              | Slower, prone to collisions, difficult to troubleshoot. |
| **Ring** | Devices form a closed loop, passing data in one direction. | Reduces collisions, efficient for certain applications. | A single failure can disrupt the network.               |
| **Mesh** | Every device connects directly to multiple others.         | Highly reliable, redundant paths prevent failures.      | Expensive, complex to manage.                           |

---

## **2. IP addressing and subnetting**

In networking, every device must have a unique identifier to communicate effectively. This identifier is called an IP address.
IP addressing enables devices to locate and exchange data across networks, whether in a small LAN or across the Internet.

To efficiently manage IP addresses, networks use subnetting, which helps divide large networks into smaller, more manageable segments.

---

### **💡 IP address**
An IP address (Internet Protocol address) is a unique numerical label assigned to each device in a network.

**It serves two primary functions –**
- Identification – Identifies a device in a network.
- Location – Specifies where the device is within a network structure.

**There are two versions of IP addresses in use –**
- IPv4 (Internet Protocol version 4) – The most widely used addressing scheme.
- IPv6 (Internet Protocol version 6) – Developed to replace IPv4 due to address exhaustion.

#### **🚀 IPv4 addressing**

An IPv4 address is a 32-bit number represented in dotted decimal format, divided into four octets (8-bit sections).

> Example – 192.168.1.1 
 
Each octet ranges from 0 to 255 (because 2^8 = 256 possible values).

#### **🚀 IPv4 Address Structure**
An IPv4 address consists of two parts:

| Address Component | Description                                           |
|-------------------|-------------------------------------------------------|
| Network portion   | Identifies the network (like a street name).          |
| Host portion      | Identifies the specific device (like a house number). |

**_Example_**  
In the IP 192.168.1.1/24,
- 192.168.1 represents the network portion.
- .1 represents the host portion (a specific device).

---

#### **🚀 IPv4 Address Classes**  
IPv4 addresses are categorized into five classes based on their starting bits.
Classes A, B, and C are used for regular networks, while Classes D and E are reserved for special purposes.

| Class | First Octet Range | Default Subnet Mask | Purpose                            |
|-------|-------------------|---------------------|------------------------------------|
| **A** | 1 – 126           | 255.0.0.0 (/8)      | Large networks (millions of hosts) |
| **B** | 128 – 191         | 255.255.0.0 (/16)   | Medium-sized networks              |
| **C** | 192 – 223         | 255.255.255.0 (/24) | Small networks                     |
| **D** | 224 – 239         | N/A                 | Multicast                          |
| **E** | 240 – 255         | N/A                 | Experimental                       |


> _**Note:**_
> - 127.x.x.x is reserved for loopback (localhost).
> - Private IP ranges (reserved for internal networks) are:
>   - Class A: 10.0.0.0 – 10.255.255.255
>   - Class B: 172.16.0.0 – 172.31.255.255
>   - Class C: 192.168.0.0 – 192.168.255.255

---

### **💡 Subnet Masks & CIDR**

A subnet mask determines which portion of an IP address represents the network and which represents the host.

> _**Example**_  
> IP Address:  192.168.1.10  
> Subnet Mask: 255.255.255.0

- 255.255.255 indicates the network.
- .0 specifies the host range.

---

#### **🚀 CIDR notation**
Classless Inter-Domain Routing (CIDR) represents subnet masks in slash notation (/ notation).

| CIDR    | Subnet Mask     | Hosts per Subnet |
|---------|-----------------|------------------|
| **/8**  | 255.0.0.0       | 16,777,214       |
| **/16** | 255.255.0.0     | 65,534           |
| **/24** | 255.255.255.0   | 254              |
| **/30** | 255.255.255.252 | 2                |

_**Example**_  
192.168.1.0/24 → Network portion: 192.168.1, Host portion: .1 to .254  
172.16.0.0/16 → Network portion: 172.16, Host portion: .0.1 to .255.254

---

### **🚀 Calculating Subnets**
Subnetting divides a network into smaller sub-networks to optimize IP usage.  
Each subnet has three important components:

| Component             | Description                                                      |
|-----------------------|------------------------------------------------------------------|
| **Network Address**   | The first IP in a subnet (e.g., `192.168.1.0/24`).               |
| **Broadcast Address** | The last IP in a subnet (e.g., `192.168.1.255/24`).              |
| **Usable Host Range** | IPs available for devices (e.g., `192.168.1.1 - 192.168.1.254`). |

---

_**Example**_  
**Given: `192.168.1.0/26`**  
Subnet mask: `255.255.255.192`

| Address Type        | IP Address   |
|---------------------|--------------|
| **Network Address** | 192.168.1.0  |
| **First Host**      | 192.168.1.1  |
| **Last Host**       | 192.168.1.62 |
| **Broadcast**       | 192.168.1.63 |

Each subnet has **62 usable hosts** (`2^6 - 2`).


## 3. Routing and Network Configuration

Routing is the process of selecting the best path for data to travel across interconnected networks. Routers, which operate at **Layer 3 (Network Layer)** of the OSI model, are responsible for making these decisions. Understanding how routers work, how routing is configured, and how to interpret network diagrams is essential for managing and troubleshooting networks effectively.

---

### 💡 Routing Fundamentals

Routers connect different networks and make decisions about where to send data based on destination IP addresses. When a packet arrives at a router, the router examines its **routing table** to determine the next hop (the next router or device) that will bring the packet closer to its final destination.

#### 🚀 How routers determine the best path

Routers use **routing tables**, which contain entries about networks the router knows about and how to reach them. Each entry includes:
- **Destination network** (e.g., 192.168.1.0/24)
- **Next hop** IP address or exit interface
- **Metric** (a value that helps choose the most efficient route)

The router compares the destination IP of the packet with its routing table entries and forwards the packet using the most specific matching route (longest prefix match).

#### 📌 Static vs. Dynamic Routing

| Type                | Description                                                               | Use Cases                                       |
|---------------------|---------------------------------------------------------------------------|-------------------------------------------------|
| **Static Routing**  | Routes are manually configured by an admin.                               | Simple networks or when full control is needed. |
| **Dynamic Routing** | Routers automatically share and update route information using protocols. | Larger or complex networks that change often.   |

##### 🛠️ Static Routing
- Manually added using commands or GUI.
- Doesn’t adapt to network failures unless manually changed.

  ``` txt
  Example: 
  ip route 192.168.2.0 255.255.255.0 192.168.1.1
  ```

##### 🔁 Dynamic Routing
- Uses routing protocols to update routes automatically.
- Adapts to topology changes and failures.
- Common protocols:
  - **RIP (Routing Information Protocol)** – distance-vector, uses hop count.
  - **OSPF (Open Shortest Path First)** – link-state, uses cost metrics.
  - **EIGRP (Enhanced Interior Gateway Routing Protocol)** – Cisco proprietary.
  - **BGP (Border Gateway Protocol)** – used between large networks and ISPs.

---

### 💡 NetPractice focus – Network Elements – Explained Simply

| Element        | What It Does                                                | How It Works                                                                                                                              |
|----------------|-------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| **Router**     | Connects different networks and decides where to send data. | Each router has **interfaces** (like ports) with IPs. It checks its **routing table** to decide which interface to send a packet through. |
| **Switch**     | Connects devices within the same LAN.                       | It forwards packets **only to the correct destination** inside the same network using MAC addresses (not used in NetPractice).            |
| **Host/PC**    | End-user devices that send and receive data.                | Each host has an **IP address** and a **default gateway** (router) it uses to talk to other networks.                                     |
| **Interface**  | A physical or virtual port on a host or router with an IP.  | Devices send/receive data **through interfaces**. If two interfaces are linked and on the same subnet, they can talk directly.            |
| **Link**       | A connection (wired or wireless) between two interfaces.    | If two interfaces are connected by a link and have compatible IPs/masks, they can communicate.                                            |
| **IP Address** | A unique identifier for a device/interface on a network.    | Used to **identify source/destination** for communication. Paired with a subnet mask to define its network.                               |


--- 

## 4. Troubleshooting (logs in NetPractice)

### 📜 NetPractice Log Messages – Full Reference

---

### ✅ Successful routing & flow

| Message                                                           | Meaning                                                                            |
|-------------------------------------------------------------------|------------------------------------------------------------------------------------|
| `on [device]: packet accepted`                                    | The device received the packet and accepted it for processing.                     |
| `on [device]: send to [interface]`                                | Packet is sent out from the device via the listed interface.                       |
| `on [device]: send to gateway [IP] through interface [interface]` | The device is forwarding the packet to a gateway using the specified interface.    |
| `on [device]: destination IP reached`                             | The packet arrived at its final destination.                                       |
| `forward way: A -> B (IP)`                                        | Start of forward path simulation, showing source, destination, and destination IP. |
| `reverse way: B -> A (IP)`                                        | Start of return path simulation.                                                   |

---

### ⚠️ Configuration warnings & intermediate issues

| Message                                                                             | Meaning                                                                                            |
|-------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| `on [device]: destination does not match any interface. pass through routing table` | The device doesn't have the destination IP on any local interface, so it checks the routing table. |
| `on [device]: route match [CIDR]`                                                   | A matching route entry was found for the destination IP.                                           |
| `on [device]: route match but no interface for gateway [IP]`                        | A route exists, but there's no interface that can reach the specified gateway.                     |
| `on switch [device]: pass to all connections`                                       | A switch is forwarding the packet to all connected devices.                                        |

---

### ❌ Failures & errors

| Message                                                           | Meaning                                                                                          |
|-------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| `on [device]: packet not for me`                                  | The packet arrived but the device determined it is not the intended recipient.                   |
| `on [device]: destination does not match any route`               | No suitable route was found in the routing table.                                                |
| `on [device]: error on destination IP - multiple interface match` | More than one interface on the device matches the destination IP → ambiguous configuration.      |
| `on [device]: error on gate IP - multiple interface match`        | More than one interface matches the gateway IP → ambiguous routing.                              |
| `on [interface]: invalid IP address`                              | The IP address set on an interface is invalid.                                                   |
| `on [interface]: invalid netmask`                                 | The subnet mask on the interface is invalid.                                                     |
| `on [device]: invalid IP on input interface [interface]`          | The receiving interface has an invalid IP during packet evaluation.                              |
| `on interface [interface]: invalid IP`                            | Interface IP can't be parsed or is not usable.                                                   |
| `on interface [interface]: invalid netmask`                       | Subnet mask is incorrectly formatted.                                                            |
| `duplicate IP ([IP])`                                             | Two interfaces have the same IP address — this causes issues.                                    |
| `private subnets not routed over internet`                        | Attempt to send private IP ranges (e.g., 192.168.x.x) over the Internet — blocked by simulation. |
| `loopback address detected on outside interface`                  | IP from 127.x.x.x (loopback) used improperly on a non-loopback interface.                        |
| `on [device]: loop detected`                                      | The packet re-entered a previously visited host, indicating a routing loop.                      |
| `invalid gate IP, route [route]`                                  | The gateway IP in a route entry is malformed.                                                    |
| `invalid route on host [device]`                                  | The route entry on a host is not in proper CIDR format or unparseable.                           |
| `invalid default route on internet [device]`                      | An invalid default route (0.0.0.0/0) was set on an Internet node, which isn’t allowed.           |

---

### 🧠 Tip for debugging

1. Look for the last device that handled the packet.
2. Watch for `no route`, `packet not for me`, or invalid IP/netmask errors — they usually show where things broke.
3. Confirm correct gateway and mask settings if routing is attempted.
4. If a device has no logs at all, the packet likely never reached it — backtrack from the previous hop.


## 📘 Glossary

> **Networking Model** – A conceptual framework that defines how data is transmitted and processed across a network by organizing communication into structured layers.

> **OSI Model** – A seven-layer model developed by the ISO that standardizes network communication by splitting it into modular layers. It helps ensure compatibility, troubleshoot issues, and design scalable networks.

> **TCP/IP Model** – A four-layer practical model used for real-world networking and the Internet. It simplifies and combines functions of the OSI model into fewer layers and is the foundation for all Internet communication.

> **Layer** – A logical level in a networking model that performs specific functions and interacts with adjacent layers only. Each layer adds or removes headers during data transfer.

> **IP Address** – A numerical label assigned to each device on a network. It identifies the device and its location on the network. Comes in IPv4 (e.g., 192.168.1.1) and IPv6 formats.

> **Subnet Mask** – A number that defines the boundary between the network and host portions of an IP address. It determines which devices are on the same local subnet.

> **CIDR (Classless Inter-Domain Routing)** – A way of writing subnet masks using a slash and number (e.g., /24), indicating how many bits are used for the network part.

> **Router** – A network device that connects different networks and makes decisions about the best path for data to travel based on routing tables.

> **Switch** – A device used in LANs that connects multiple devices and intelligently forwards data only to the intended recipient device.

> **Hub** – A legacy network device that connects multiple devices but broadcasts data to all ports, making it less efficient than a switch.

> **Access Point (AP)** – A device that allows wireless devices to connect to a wired network using Wi-Fi.

> **Interface** – A physical or virtual port on a device (like a router or host) used to send or receive network traffic. Each interface typically has an IP address.

> **Link** – A connection between two devices or interfaces, either physical (like a cable) or virtual, allowing data transfer between them.

> **Routing Table** – A data table stored in routers that lists known networks and the next hop/interface to reach each destination.

> **Static Route** – A manually configured path for network traffic used by a router to reach specific destinations.

> **Dynamic Routing** – A method where routers automatically exchange information and adjust routes using routing protocols like RIP or OSPF.

> **Default Gateway** – The router that a device sends data to when the destination is outside its own network/subnet.

> **Encapsulation** – The process of wrapping data with protocol-specific headers as it moves down the layers of a network model.

> **Decapsulation** – The process of removing protocol headers as data moves up through the layers on the receiving side.

> **Private IP Address** – IP ranges reserved for internal network use, not routable on the public Internet (e.g., 192.168.x.x, 10.x.x.x, 172.16–31.x.x).

> **Public IP Address** – An IP address that is globally routable on the Internet, assigned by an ISP or authority like IANA.

> **MAC Address** – A hardware address assigned to network interfaces, used for local communication within a LAN (used by switches, not routers).

> **Ping** – A network diagnostic tool that sends an ICMP echo request to test if a host is reachable and how long it takes to respond.

> **Traceroute** – A tool used to track the path data takes from source to destination by listing all the routers it passes through.
