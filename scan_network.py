from scapy.all import ARP, Ether, srp
import re


def scan_network(ip_range):
    # Create an ARP request packet
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address

    # Combine ARP request and Ethernet frame
    packet = ether / arp

    # Send the packet and get the responses
    result = srp(packet, timeout=3, verbose=0)[0]

    # Parse the results
    devices = []
    for sent, received in result:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    return devices


def find_esp32(devices):
    # Update this to match the actual MAC address prefix of your ESP32
    esp32_mac_prefix = "18:fe:34"  # Change to match your ESP32 MAC address prefix

    for device in devices:
        if device["mac"].lower().startswith(esp32_mac_prefix):
            return device

    return None


if __name__ == "__main__":
    # Use your determined network range
    ip_range = "192.168.0.0/24"  # Adjust this according to your network

    print("Scanning network...")
    devices = scan_network(ip_range)

    if devices:
        print(f"Found {len(devices)} devices.")
        print("Detected devices:")
        for device in devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}")

        esp32_device = find_esp32(devices)

        if esp32_device:
            print(
                f"ESP32 found at IP: {esp32_device['ip']}, MAC: {esp32_device['mac']}"
            )
        else:
            print("ESP32 not found.")
    else:
        print("No devices found.")
