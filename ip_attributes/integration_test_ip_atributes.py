import subprocess
import re
import ipaddress


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


total_tests = 0
passed_tests = 0


def run_program_with_args(*args):
    """
    Runs the main IP subnet program with the given arguments.
    Captures and returns the stdout output.
    Used to simulate CLI usage from tests.
    """
    result = subprocess.run(
        ["python3", "ip_subnet_props.py", *args],
        text=True,
        capture_output=True
    )
    return result.stdout.strip()


def parse_output(output):
    """
      Parses output lines like 'Key: Value' into a dictionary.
      Strips whitespace and ignores empty lines.
      Used to extract values for comparison.
      """
    result = {}
    for line in output.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            result[key.strip()] = value.strip()
    return result


def validate_with_ipaddress(ip, cidr, output):
    """
        Cross-validates program output with Python's ipaddress module.
        Calculates expected network attributes, including usable host count.
        Compares and prints OK/KO results for each key.
    """
    global total_tests, passed_tests
    expected = {}
    net = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)

    expected["Network address"] = str(net.network_address)
    expected["Broadcast address"] = str(net.broadcast_address)
    expected["Subnet mask"] = str(net.netmask)
    expected["CIDR"] = f"/{net.prefixlen}"
    expected["Number of usable hosts"] = str(max(0, net.num_addresses))

    hosts = list(net.hosts())

    # Usable hosts logic
    if cidr == 32:
        usable_hosts = 0
    elif cidr == 31:
        usable_hosts = 2  # Or 0 if you want strict legacy behavior
    else:
        usable_hosts = max(0, net.num_addresses - 2)

    expected["Number of usable hosts"] = str(usable_hosts)

    hosts = list(net.hosts())

    if cidr == 31 and len(hosts) == 2:
        expected["First usable IP"] = str(hosts[0])
        expected["Last usable IP"] = str(hosts[1])
    elif cidr == 32 or len(hosts) == 0:
        expected["First usable IP"] = str(net.network_address)
        expected["Last usable IP"] = str(net.network_address)
    else:
        expected["First usable IP"] = str(hosts[0])
        expected["Last usable IP"] = str(hosts[-1])

    group_size = 2 ** (32 - cidr)
    expected["Subnet group size"] = str(group_size)

    next_net = int(net.network_address) + group_size
    prev_net = int(net.network_address) - group_size

    expected["Next network address"] = (
        "No next network" if next_net > 0xFFFFFFFF else str(ipaddress.IPv4Address(next_net))
    )
    expected["Previous network address"] = (
        "No previous network" if prev_net < 0 else str(ipaddress.IPv4Address(prev_net))
    )

    parsed = parse_output(output)

    print("\n  Cross-check with ipaddress module:")
    print("  ----------------------------------")
    all_ok = True
    for key in expected:
        actual = parsed.get(key)
        correct = expected[key]
        if actual == correct:
            print(f"  {key:<25}:{GREEN}OK{RESET} {actual}")
        else:
            print(f"  {key:<25}:{RED}KO{RESET} Program value: {actual} | Expected: {correct}{RESET}")
            all_ok = False
    if all_ok:
        passed_tests += 1


def test_case(name, args, expected_output_snippets):
    """
       Runs a test by executing the program and checking expected substrings.
       Uses basic string inclusion instead of structured parsing.
    """
    global total_tests, passed_tests
    total_tests += 1
    print(f"\n{name} ... ", end="")
    output = run_program_with_args(*args)
    if all(expected in output for expected in expected_output_snippets):
        print(f"{GREEN}OK{RESET}")
        passed_tests += 1
    else:
        print(f"{RED}KO{RESET}")
        print("Args:", args)
        print("Output:\n", output)
        print("Expected to include:")
        for line in expected_output_snippets:
            print(f"  - {line}")


def test_valid_case_with_reference(name, ip, cidr):
    """
       Runs a test and compares output with ipaddress module logic.
       Internally uses `validate_with_ipaddress` for detailed checking.
       Prints result and any mismatched fields.
    """
    global total_tests, passed_tests
    total_tests += 1
    print(f"\n{name} ... ", end="")
    output = run_program_with_args(f"{ip}/{cidr}")
    validate_with_ipaddress(ip, cidr, output)
    print("\n")


def extract_fyi_blocks(output):
    """
        Checks whether the FYI block includes all expected categories.
        Extracts 'Category' labels and compares against expectation.
    """
    fyi_blocks = []
    in_fyi = False
    current = []

    for line in output.splitlines():
        if "---------- FYI ----------" in line:
            in_fyi = True
            continue
        if in_fyi:
            if "-------------------------" in line:
                break
            elif line.strip() == "":
                if current:
                    fyi_blocks.append("\n".join(current).strip())
                    current = []
            else:
                current.append(line.strip())

    if current:
        fyi_blocks.append("\n".join(current).strip())

    return fyi_blocks


def test_fyi_output(name, args, expected_categories):
    """
        Runs all integration and validation tests.
        Includes valid cases, invalid formats, edge cases, and FYI validation.
        Tracks and reports overall pass/fail counts at the end.
    """
    global total_tests, passed_tests
    total_tests += 1
    print(f"\n{name} ... ", end="")
    output = run_program_with_args(*args)
    fyi_blocks = extract_fyi_blocks(output)

    categories_found = [block.splitlines()[0].replace("Category: ", "").strip() for block in fyi_blocks]

    missing = [c for c in expected_categories if c not in categories_found]
    unexpected = [c for c in categories_found if c not in expected_categories]

    if not missing and not unexpected:
        print(f"{GREEN}OK{RESET}")
        passed_tests += 1
    else:
        print(f"{RED}KO{RESET}")
        print("Args:", args)
        print("FYI Categories Found:", categories_found)
        if missing:
            print(f"Missing expected categories: {missing}")
        if unexpected:
            print(f"Unexpected categories: {unexpected}")


def run_all_tests():
    print("\n#####################################\n### Running CLI Integration Tests "
          "###\n#####################################")

    # --- Valid input tests ---
    test_case("CIDR input: 10.10.0.0/19", ["10.10.0.0/19"], [
        "Network address: 10.10.0.0",
        "Broadcast address: 10.10.31.255",
        "Subnet mask: 255.255.224.0",
        "CIDR: /19",
        "Number of usable hosts: 8190",
        "First usable IP: 10.10.0.1",
        "Last usable IP: 10.10.31.254",
        "Subnet group size: 8192",
        "Next network address: 10.10.32.0",
        "Previous network address: 10.9.224.0"
    ])

    test_case("Subnet mask input: 10.10.0.0 255.255.255.0", ["10.10.0.0", "255.255.255.0"], [
        "Network address: 10.10.0.0",
        "Broadcast address: 10.10.0.255",
        "Subnet mask: 255.255.255.0",
        "CIDR: /24",
        "Number of usable hosts: 254",
        "First usable IP: 10.10.0.1",
        "Last usable IP: 10.10.0.254",
        "Subnet group size: 256",
        "Next network address: 10.10.1.0",
        "Previous network address: 10.9.255.0"
    ])

    test_case("CIDR input: 192.168.1.0/30", ["192.168.1.0/30"], [
        "Network address: 192.168.1.0",
        "Broadcast address: 192.168.1.3",
        "Subnet mask: 255.255.255.252",
        "CIDR: /30",
        "Number of usable hosts: 2",
        "First usable IP: 192.168.1.1",
        "Last usable IP: 192.168.1.2",
        "Subnet group size: 4",
        "Next network address: 192.168.1.4",
        "Previous network address: 192.168.0.252"
    ])

    # --- Invalid IPs (preserve specific messages for IPs) ---
    test_case("Invalid IP: octet > 255", ["192.168.300.1", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: negative octet", ["192.168.-1.1", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: leading zeros", ["192.168.01.1", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: too many octets", ["192.168.1.1.5", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: too few octets", ["192.168.1", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: only dots", ["...", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: contains letters", ["192.168.1.a", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: space between octets", ["192.168.1. 1", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: 256", ["192.168.1.256", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: all octets bad", ["256.256.256.256", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: wrong delimiter", ["192,168,1,1", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: mixed errors", ["192.168.300.-1", "/24"], ["Error: Invalid IP format."])
    test_case("Invalid IP: trailing dot", ["192.168.1.1.", "/24"], ["Error: Invalid IP format."])

    # --- Subnet mask errors (generalized format error) ---
    test_case("Mask too many octets", ["192.168.1.1", "255.255.255.255.0"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask too few octets", ["192.168.1.1", "255.255.255"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask negative", ["192.168.1.1", "-255.255.255.0"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask non-numeric", ["192.168.1.1", "255.abc.255.0"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask leading zeros", ["192.168.1.1", "255.255.0255.0"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask out of range", ["192.168.1.1", "255.500.255.0"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask invalid block", ["192.168.1.1", "255.255.64.0"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask only dots", ["192.168.1.1", "..."],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask commas instead of dots", ["192.168.1.1", "255,255,255,0"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask with spaces", ["192.168.1.1", "255. 255.255.0"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask empty", ["192.168.1.1", ""],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("Mask with trailing dot", ["192.168.1.1", "255.255.255.0."],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])

    # --- CIDR validation (generalized format error) ---
    test_case("CIDR with spaces", ["192.168.1.1", " / 24 "],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("CIDR without slash", ["192.168.1.1", "24"], ["CIDR: /24"])  # allowed
    test_case("CIDR negative", ["192.168.1.1", "/-24"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("CIDR non-numeric", ["192.168.1.1", "/abc"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("CIDR leading zero", ["192.168.1.1", "/024"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("CIDR too low", ["192.168.1.1", "/-1"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("CIDR empty", ["192.168.1.1", ""],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("CIDR with extra characters", ["192.168.1.1", "/24abc"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])
    test_case("CIDR wrong delimiter", ["192.168.1.1", ",24"],
              ["Error: Invalid CIDR/mask format. Expected: /<0–31> or valid subnet mask"])

    # --- Next/previous network edge ---
    test_case("Next net: 255.255.255.0/24", ["255.255.255.0/24"], ["Next network address: No next network"])
    test_case("Prev net: 0.0.0.0/24", ["0.0.0.0/24"], ["Previous network address: No previous network"])

    # --- Assert equal with python ipaddress module ---
    test_valid_case_with_reference("Cross-validate: 192.168.1.0/30", "192.168.1.0", 30)

    # This test runs, but takes a lot of time
    # test_valid_case_with_reference("Cross-validate: 10.0.0.0/8", "10.0.0.0", 8)

    test_valid_case_with_reference("Cross-validate: 172.16.0.0/12", "172.16.0.0", 12)
    test_valid_case_with_reference("Cross-validate: 192.168.0.0/16", "192.168.0.0", 16)
    test_valid_case_with_reference("Cross-validate: 192.168.123.128/25", "192.168.123.128", 25)
    test_valid_case_with_reference("Cross-validate: 192.168.123.0/26", "192.168.123.0", 26)
    test_valid_case_with_reference("Cross-validate: 192.168.123.192/26", "192.168.123.192", 26)
    test_valid_case_with_reference("Cross-validate: 203.0.113.0/30", "203.0.113.0", 30)
    test_valid_case_with_reference("Cross-validate: 198.51.100.4/31", "198.51.100.4", 31)
    test_valid_case_with_reference("Cross-validate: 198.51.100.0/32", "198.51.100.0", 32)

    # --- FYI section testing---
    test_fyi_output(
        "FYI: Private + Special CIDR /31",
        ["192.168.1.0/31"],
        ["Private IP address", "Special CIDR"]
    )

    test_fyi_output(
        "FYI: Special CIDR /32 only",
        ["203.0.113.5/32"],
        ["Special CIDR"]
    )

    test_fyi_output(
        "FYI: Private range only",
        ["10.10.10.10/24"],
        ["Private IP address"]
    )

    test_fyi_output(
        "FYI: Loopback",
        ["127.0.0.1/8"],
        ["Loopback IP address"]
    )

    print("\n#####################################")
    print(f"Tests run: {total_tests}")
    print(f"{GREEN}Tests passed: {passed_tests}")
    print(f"{RED}Tests failed: {total_tests - passed_tests}{RESET}")
    print("#####################################\n")


if __name__ == "__main__":
    run_all_tests()
