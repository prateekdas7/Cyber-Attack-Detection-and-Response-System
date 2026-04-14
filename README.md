# \# Cyberattack Detection and Response System

# 

# A Python-based system that captures network packets in real-time, detects DoS and SYN flood attacks, and provides AI-generated countermeasures using Llama 3.2.

# 

# \## Overview

# 

# This project integrates \*\*Wireshark\*\* (via `tshark`) for packet capture and analysis, \*\*Scapy\*\* for packet inspection, and \*\*Llama 3.2\*\* (via Ollama) for generating context-sensitive countermeasure recommendations. When an attack is detected, the system alerts the user with a desktop notification and displays recommended countermeasures in a GUI window.

# 

# \### Attack Types Detected

# 

# | Scenario | Detection Criteria | Response |

# |---|---|---|

# | Ping Flood / DoS | Average packets/sec > 100 | Notification + AI countermeasures |

# | SYN Flood | SYN packet count > 50 | Notification + AI countermeasures |

# | Normal Traffic | Below thresholds | "No danger detected" |

# 

# \## Architecture

# 

# ```

# Internet → Wireshark (tshark) → Packet Capture (.pcapng)

# &#x20;                                       ↓

# &#x20;                                 Detection Engine (Scapy)

# &#x20;                                       ↓

# &#x20;                             ┌─────────┴─────────┐

# &#x20;                             ↓                   ↓

# &#x20;                    Notification            Countermeasure

# &#x20;                    (plyer)              Generation (Llama 3.2)

# &#x20;                             ↓                   ↓

# &#x20;                             └─────────┬─────────┘

# &#x20;                                       ↓

# &#x20;                                  User Interface

# &#x20;                                  (Tkinter GUI)

# ```

# 

# \## Prerequisites

# 

# \- \*\*Python 3.8+\*\*

# \- \*\*Wireshark\*\* — installed with `tshark` command-line utility

# &#x20; - \[Download Wireshark](https://www.wireshark.org/download.html)

# \- \*\*Ollama\*\* — for running Llama 3.2 locally

# &#x20; - \[Download Ollama](https://ollama.ai/)

# &#x20; - After installing, pull the model: `ollama pull llama3.2`

# 

# \- \*\*Tkinter\*\* — included with most Python installations. If missing on Linux:

# &#x20; ```bash

# &#x20; sudo apt install python3-tk

# &#x20; ```

# 

# \## Installation

# 

# 1\. \*\*Clone the repository\*\*

# &#x20;  ```bash

# &#x20;  git clone https://github.com/<your-username>/cyberattack-detection-response.git

# &#x20;  cd cyberattack-detection-response

# &#x20;  ```

# 

# 2\. \*\*Install Python dependencies\*\*

# &#x20;  ```bash

# &#x20;  pip install -r requirements.txt

# &#x20;  ```

# 

# 3\. \*\*Configure tshark path\*\*

# 

# &#x20;  In `detection.py`, update the tshark path to match your installation:

# &#x20;  ```python

# &#x20;  # Windows (default)

# &#x20;  r"C:\\Program Files\\Wireshark\\tshark.exe"

# 

# &#x20;  # Linux

# &#x20;  "tshark"

# 

# &#x20;  # macOS (Homebrew)

# &#x20;  "/usr/local/bin/tshark"

# &#x20;  ```

# 

# 4\. \*\*Start Ollama\*\*

# &#x20;  ```bash

# &#x20;  ollama serve

# &#x20;  ```

# 

# \## Usage

# 

# Run the detection and response system:

# 

# ```bash

# python response.py

# ```

# 

# This will:

# 1\. Capture network packets on the Wi-Fi interface for 10 seconds

# 2\. Analyze captured packets for DoS / SYN flood indicators

# 3\. Export packet data to `packets.xlsx`

# 4\. If an attack is detected:

# &#x20;  - Display a desktop notification

# &#x20;  - Query Llama 3.2 for countermeasures

# &#x20;  - Show countermeasures in a GUI popup

# 

# You can also run detection standalone:

# 

# ```bash

# python detection.py

# ```

# 

# \### Configuration

# 

# You can adjust detection parameters in `detection.py`:

# 

# ```python

# capture\_with\_tshark(file\_name='sample.pcapng', duration=10, interface='Wi-Fi')

# detect\_dos\_attack(packets, duration=10, threshold=100, syn\_threshold=50)

# ```

# 

# \- `duration` — capture time in seconds

# \- `threshold` — packets/sec to flag a DoS attack

# \- `syn\_threshold` — SYN packet count to flag a SYN flood

# \- `interface` — network interface to monitor (e.g., `Wi-Fi`, `eth0`)

# 

# \## Project Structure

# 

# ```

# ├── detection.py        # Packet capture, attack detection, and Excel export

# ├── response.py         # AI countermeasure generation, notifications, and GUI

# ├── requirements.txt    # Python dependencies

# ├── sample.pcapng       # Sample packet capture file (generated at runtime)

# ├── packets.xlsx        # Sample exported packet data

# └── README.md

# ```

# 

# \## How It Works

# 

# \*\*Detection Module (`detection.py`)\*\*

# \- Uses `tshark` to capture live network traffic into a `.pcapng` file

# \- Reads packets with Scapy and calculates average packet rate and SYN packet count

# \- Flags traffic as a potential DoS attack if packets/sec exceed the threshold

# \- Flags traffic as a potential SYN flood if SYN packets exceed the SYN threshold

# \- Exports all packet details (timestamp, IPs, protocol, ports, length) to an Excel file

# 

# \*\*Response Module (`response.py`)\*\*

# \- Retrieves the detection result from `detection.py`

# \- Sends the attack type to Llama 3.2 via Ollama's local API

# \- Receives AI-generated countermeasures (e.g., rate limiting, IP blocking, firewall rules)

# \- Displays a desktop notification alerting the user

# \- Opens a Tkinter GUI window with the full list of countermeasures

# 

# \## Technologies

# 

# \- \*\*Python 3\*\* — core language

# \- \*\*Scapy\*\* — packet reading and analysis

# \- \*\*Wireshark / tshark\*\* — network packet capture

# \- \*\*Pandas\*\* — data manipulation and Excel export

# \- \*\*Ollama + Llama 3.2\*\* — AI-powered countermeasure generation

# \- \*\*Plyer\*\* — cross-platform desktop notifications

# \- \*\*Tkinter\*\* — GUI for displaying countermeasures

# 

# \## Limitations

# 

# \- Detection uses simple threshold-based rules — may miss low-volume or sophisticated attacks

# \- Countermeasure generation depends on a running Ollama instance

# \- Currently monitors only TCP, UDP, and ICMP protocols

# \- Requires manual tshark path configuration per platform

# 

# \## Future Improvements

# 

# \- Machine learning-based detection for broader attack coverage

# \- Automated response actions (firewall rule injection, IP blocking)

# \- Dashboard-style GUI with traffic visualizations

# \- Support for additional protocols (HTTP, DNS, FTP)

# \- Offline countermeasure knowledge base for reduced latency

# 

# \## Authors

# 

# \- P Revant Kumar (21BCE0310)

# \- Luniya Rishi Rahul (21BCE2350)

# \- Prateek Das (21BCE2875)

# 

# Supervised by \*\*Dr. Saritha Murali\*\*, VIT — School of Computer Science and Engineering (SCOPE)

# 

# \## License

# 

# This project was developed as part of the BCSE497J (Project-I) course at VIT, Vellore.

