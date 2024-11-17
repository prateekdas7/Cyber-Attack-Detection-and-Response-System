# file1.py

import subprocess
from scapy.all import rdpcap, TCP
import pandas as pd
import os
import time

def capture_with_tshark(file_name='sample.pcapng', duration=10, interface='Wi-Fi'):
    # Remove the file if it already exists to avoid conflicts
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
        except PermissionError:
            print(f"{file_name} is currently in use. Waiting for it to become available...")
            time.sleep(1)
            os.remove(file_name)

    # Run tshark to capture packets for a specified duration from the selected interface
    print(f"Starting Wireshark capture on {interface} for {duration} seconds...")
    subprocess.run(
        [r"D:\wireshark\tshark.exe", "-i", interface, "-a", f"duration:{duration}", "-w", file_name],
        check=True
    )

    time.sleep(2)  # Wait for tshark to fully release the file
    print(f"Capture completed and saved to {file_name}")



def detect_dos_attack(packets, duration=10, threshold=100, syn_threshold=50):
    total_packets = len(packets)
    avg_packets_per_second = total_packets / duration
    
    print(f"Average packets per second: {avg_packets_per_second}")
    syn_count = sum(1 for packet in packets if packet.haslayer(TCP) and packet[TCP].flags == 'S')
    print(f"SYN packets count: {syn_count}")

    if avg_packets_per_second > threshold:
        print("Potential DoS attack detected!")
        
        return "dos attack"
    
    if syn_count > syn_threshold:
        print("Potential SYN flood attack detected!")
        return "Syn attack"
    
    print("Traffic appears normal.")
    print("No danger detected")
    return "dos attack"

def convert_pcapng_to_excel(file_path, output_excel):
    packets = rdpcap(file_path)
    
    packet_data = {
        "Packet Number": [],
        "Timestamp": [],
        "Source IP": [],
        "Destination IP": [],
        "Protocol": [],
        "Source Port": [],
        "Destination Port": [],
        "Length": []
    }

    for i, packet in enumerate(packets):
        packet_data["Packet Number"].append(i + 1)
        packet_data["Timestamp"].append(packet.time if hasattr(packet, 'time') else 'N/A')
        packet_data["Source IP"].append(packet["IP"].src if packet.haslayer("IP") else 'N/A')
        packet_data["Destination IP"].append(packet["IP"].dst if packet.haslayer("IP") else 'N/A')
        
        if packet.haslayer("TCP"):
            protocol = "TCP"
            packet_data["Source Port"].append(packet["TCP"].sport)
            packet_data["Destination Port"].append(packet["TCP"].dport)
        elif packet.haslayer("UDP"):
            protocol = "UDP"
            packet_data["Source Port"].append(packet["UDP"].sport)
            packet_data["Destination Port"].append(packet["UDP"].dport)
        elif packet.haslayer("ICMP"):
            protocol = "ICMP"
            packet_data["Source Port"].append('N/A')
            packet_data["Destination Port"].append('N/A')
        else:
            protocol = "Other"
            packet_data["Source Port"].append('N/A')
            packet_data["Destination Port"].append('N/A')
        
        packet_data["Protocol"].append(protocol)
        packet_data["Length"].append(len(packet))

    df = pd.DataFrame(packet_data)
    df.to_excel(output_excel, index=False)
    print(f"Packet data has been saved to {output_excel}")

# Main execution
sample_pcapng = 'sample.pcapng'
output_excel = 'packets.xlsx'

capture_with_tshark(file_name=sample_pcapng, duration=10, interface='Wi-Fi')
packets = rdpcap(sample_pcapng)
attack_result = detect_dos_attack(packets, duration=10, threshold=100, syn_threshold=50)
convert_pcapng_to_excel(sample_pcapng, output_excel)

# Export the result for use in file2.py
def get_attack_result():
    return attack_result