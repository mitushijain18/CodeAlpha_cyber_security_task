from scapy.all import sniff

def process_packet(packet):
    print("\n--- Packet Captured ---")

    if packet.haslayer("IP"):
        print("Source IP:", packet["IP"].src)
        print("Destination IP:", packet["IP"].dst)
        print("Protocol:", packet["IP"].proto)

    print(packet.summary())

print("Starting Network Sniffer...")
sniff(prn=process_packet, count=10)

print("\nCapture Completed!")