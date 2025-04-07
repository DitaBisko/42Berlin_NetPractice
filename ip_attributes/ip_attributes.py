import sys
import re
import json
import textwrap


class Subnet:
    """
      Represents a subnet and provides detailed calculations for:
      - Network and broadcast addresses
      - Usable host range and count
      - Subnet group size and adjacent networks
    """
    def __init__(self, ip, cidr):
        self.ip = ip
        self.cidr = cidr
        self.mask = self.cidr_to_mask()
        self.binary_mask = self.convert_4_octets_to_binary(self.mask)
        self.binary_ip = self.convert_4_octets_to_binary(self.ip)

        self.network_address = int(self.binary_ip, 2) & int(self.binary_mask, 2)
        binary_mask_int = int(self.binary_mask, 2)
        self.broadcast_address = self.network_address | (~binary_mask_int & 0xFFFFFFFF)

        self.first_usable_ip, self.last_usable_ip, self.usable_hosts = self.calculate_usable_range()

    def calculate_usable_range(self):
        """
            Determines the first and last usable IPs in the subnet.
            Usable hosts = total - 2, unless /31 or /32 (special rules).
        """
        if self.cidr == 32:
            return self.network_address, self.network_address, 0
        elif self.cidr == 31:
            return self.network_address, self.broadcast_address, 2
        else:
            first_ip = self.network_address + 1
            last_ip = self.broadcast_address - 1
            usable = self.broadcast_address - self.network_address - 1
            return first_ip, last_ip, usable

    def cidr_to_mask(self):
        """
            Converts CIDR into dotted-decimal subnet mask.
            e.g. /24 -> 255.255.255.0
        """
        binary = self.cidr_to_binary()
        octets = [binary[i:i + 8] for i in range(0, 32, 8)]
        decimal_octets = [str(int(octet, 2)) for octet in octets]
        return ".".join(decimal_octets)

    def calculate_next_network(self):
        """
            Gets the base address of the next subnet.
            Adds subnet group size to current network address.
        """
        next_network = self.network_address + self.snet_group_size()
        if next_network > 0xFFFFFFFF:
            return "No next network"
        return self.int_to_dotted_decimal(next_network)

    def calculate_previous_network(self):
        """
           Gets the base address of the previous subnet.
           Subtracts subnet group size from current network.
        """
        previous_network = self.network_address - self.snet_group_size()
        if previous_network < 0:
            return "No previous network"
        return self.int_to_dotted_decimal(previous_network)

    def snet_group_size(self):
        """
           Subnet group size = 2^(32 - CIDR).
           Total number of IPs in the subnet (including net/broadcast).
        """
        return 2 ** (32 - self.cidr)

    def cidr_boundary_octet(self):
        """
            Returns which octet the CIDR boundary ends in.
            Used for step-size or formatting logic.
        """
        return (self.cidr - 1) // 8

    def subnet_step(self):
        """
            Calculates increment step size per subnet.
            Based on remaining bits in final octet.
        """
        bits_used = self.cidr % 8
        if bits_used == 0:
            return 256
        return 2 ** (8 - bits_used)

    def cidr_to_binary(self):
        """
           Converts CIDR into 32-bit binary mask string.
           e.g. /24 => '11111111111111111111111100000000'
       """
        return "1" * self.cidr + "0" * (32 - self.cidr)

    @staticmethod
    def convert_4_octets_to_binary(octets):
        """
           Converts dotted decimal IP or mask to a binary string.
           e.g. 255.255.255.0 => '11111111111111111111111100000000'
        """
        octets = octets.split(".")
        return "".join(bin(int(octet))[2:].zfill(8) for octet in octets)

    @staticmethod
    def int_to_dotted_decimal(binary_int):
        """
            Converts a 32-bit integer to dotted-decimal IP format.
            e.g. 3232235776 => '192.168.1.0'
        """
        binary_str = bin(binary_int)[2:].zfill(32)
        octets = [binary_str[i:i+8] for i in range(0, 32, 8)]
        return ".".join(str(int(octet, 2)) for octet in octets)

    @staticmethod
    def octets_to_dotted_decimal(octets):
        """
            Converts a list of octets into dotted string.
            e.g. [192, 168, 1, 1] => '192.168.1.1'
        """
        return ".".join(str(o) for o in octets)

    def print_info(self):
        """
            Outputs all computed subnet information and FYI data.
        """
        print("\n----- IP Attributes -----\n")
        print(f"Network address: {self.int_to_dotted_decimal(self.network_address)}")
        print(f"Broadcast address: {self.int_to_dotted_decimal(self.broadcast_address)}")
        print(f"Subnet mask: {self.mask}")
        print(f"CIDR: /{self.cidr}")
        print(f"Number of usable hosts: {self.usable_hosts}")
        print(f"First usable IP: {self.int_to_dotted_decimal(self.first_usable_ip)}")
        print(f"Last usable IP: {self.int_to_dotted_decimal(self.last_usable_ip)}")
        print(f"Subnet group size: {self.snet_group_size()}")
        print(f"Next network address: {self.calculate_next_network()}")
        print(f"Previous network address: {self.calculate_previous_network()}")

        # Load special ranges from JSON
        special_ranges = load_special_ranges()
        # Pass self.cidr so that get_fyi_info can also check for a CIDR-specific entry
        fyi_list = get_fyi_info(self.ip, special_ranges, self.cidr)
        if fyi_list:
            print("\n---------- FYI ----------")
            for fyi in fyi_list:
                print(f"Category: {fyi['category']}")
                wrapped_usage = textwrap.fill(
                    fyi['usage'],
                    width=70,
                    initial_indent="Usage  : ",
                    subsequent_indent="         "
                )
                print(wrapped_usage)
                print()  # Add spacing between FYI blocks
        else:
            print("\n-------------------------\n")


def load_special_ranges(filename="reserved_ip.json"):
    """
        Loads JSON file containing reserved and special-use IP ranges.
        Used to provide FYI info based on input IP or CIDR.
    """
    with open(filename, "r") as file:
        return json.load(file)


def ip_to_int(ip_str):
    """
        Converts an IP string to a 32-bit integer.
        e.g. '192.168.1.1' => 3232235777
    """
    octets = [int(o) for o in ip_str.strip().split(".")]
    return (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]


CATEGORY_PRIORITY = {
    # Determines which category has higher priority for display
    "Loopback IP address": 1,
    "Link-local IP address": 2,
    "Special CIDR": 3,
    "Private IP address": 4,
    "Reserved IP address": 5,
    "Multicast IP address": 6,
    "Public DNS (Google) IP address": 7,
    "Public DNS (Cloudflare) IP address": 8,
    "Public DNS (Quad9) IP address": 9,
}


def get_fyi_info(ip_str, special_ranges, cidr=None):
    """
        Matches input IP against reserved IP ranges and special CIDRs.
        Returns the most relevant category and optional CIDR match.
        Uses priority sorting to prefer most relevant category.
    """
    ip_int = ip_to_int(ip_str)
    ip_matches = []
    cidr_matches = []
    for entry in special_ranges:
        try:
            if "cidr" in entry and entry["cidr"] != "N/A":
                if cidr is not None and entry["cidr"] == f"/{cidr}" and entry["range"] == "any":
                    cidr_matches.append(entry)
                    continue
            if " - " in entry["range"]:
                start_str, end_str = entry["range"].split(" - ")
                start_int = ip_to_int(start_str)
                end_int = ip_to_int(end_str)
                if start_int <= ip_int <= end_int:
                    ip_matches.append(entry)
            else:
                if ip_str.strip() == entry["range"].strip():
                    ip_matches.append(entry)
        except Exception:
            continue
    ip_matches.sort(key=lambda x: CATEGORY_PRIORITY.get(x["category"], 999))
    top_ip_category = CATEGORY_PRIORITY.get(ip_matches[0]["category"], 999) if ip_matches else None
    top_ip_matches = [entry for entry in ip_matches if CATEGORY_PRIORITY.get(entry["category"], 999) == top_ip_category]
    return top_ip_matches + cidr_matches


def subnet_to_cidr(subnet_mask):
    """
        Converts subnet mask (e.g., 255.255.255.0) to CIDR (e.g., /24).
        Validates binary continuity (no "01" patterns allowed).
    """
    subnet_mask = subnet_mask.strip()
    octets = subnet_mask.split(".")
    if len(octets) != 4:
        raise ValueError("Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask.")
    for octet in octets:
        if not octet.isdigit():
            raise ValueError("Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask.")
        if octet != str(int(octet)):
            raise ValueError("Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask.")
        if not (0 <= int(octet) <= 255):
            raise ValueError("Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask.")
    binary_mask = ''.join(f'{int(o):08b}' for o in octets)
    if "01" in binary_mask:
        raise ValueError("Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask.")
    cidr = binary_mask.count("1")
    return cidr


def main(argc, argv):
    """
        Parses and validates CLI arguments.
        Accepts IP/CIDR, IP + CIDR, or IP + subnet mask.
        Runs the Subnet class and prints output.
    """
    try:
        if argc == 2:
            arg = argv[1].strip()
            match = re.match(r'^(\d{1,3}(?:\.\d{1,3}){3})\s*/\s*(\d{1,2})$', arg)
            if not match:
                raise ValueError("Error: Invalid input format. Expected IP/CIDR like '192.168.0.1/24'.")
            ip, cidr_str = match.groups()
        elif argc == 3:
            ip = argv[1].strip()
            second_arg = argv[2].strip()
            # Validate IP using regex
            if not re.fullmatch(r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)"
                                r"(\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}", ip):
                raise ValueError("Error: Invalid IP format.")
            if any(o != str(int(o)) for o in ip.split(".")):
                raise ValueError("Error: Invalid IP format.")  # leading zeros
            cidr_match = re.fullmatch(r"/?(\d{1,2})", second_arg)
            if cidr_match:
                cidr_str = cidr_match.group(1)
            else:
                # Try subnet mask
                try:
                    cidr = subnet_to_cidr(second_arg)
                except Exception:
                    raise ValueError("Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask.")

                subnet = Subnet(ip, cidr)
                subnet.print_info()
                return
        else:
            raise ValueError("Error: Usage: <program> <ip/cidr> OR <ip> <subnet mask> OR <ip> /cidr")
        if not re.fullmatch(r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)"
                            r"(\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}", ip):
            raise ValueError("Error: Invalid IP format.")
        if any(o != str(int(o)) for o in ip.split(".")):
            raise ValueError("Error: Invalid IP format.")  # leading zeros
        if not cidr_str.isdigit() or not (0 <= int(cidr_str) <= 32):
            raise ValueError("Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask.")
        cidr = int(cidr_str)

        subnet = Subnet(ip, cidr)
        subnet.print_info()

    except ValueError as msg:
        print(msg)
    except Exception as msg:
        print(f"Unexpected error: {msg}")


if __name__ == '__main__':
    argc = len(sys.argv)
    argv = sys.argv
    main(argc, argv)
