import socket
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="Simple Port Scanner")
parser.add_argument('--ip', required=False, default='192.168.1.254', help='IP address to scan (default: 192.168.1.254)')
parser.add_argument('--port', type=int, required=False, help='Specify a specific port to scan')
parser.add_argument('--range', required=False, default='1-200', help='Specify range to scan (default: 1-200)')
parser.add_argument('--sv', required=False, action='store_true', help='Saves results to to a txt file (filename based on date)')
parser.add_argument('--name', required=False, help='Name for output file')
#to add: output file, ouput mode (print/save only open, closed, both)
args = parser.parse_args()

def ScanPort(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    
    if result == 0:
        print(f"Port {port} on {ip} is OPEN")
        return (port, True)
    else:
        print(f"Port {port} on {ip} is CLOSED")
        return (port, False)
        
def ScanRange(ip, inputRange):
    minRange, maxRange = map(int, inputRange.split('-'))
    portList = list(range(minRange, maxRange + 1))
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(lambda port: ScanPort(ip, port), portList))
    return results

def Output(filename):
    print(f"Output file saved as {filename}")

if args.port:
    results = [ScanPort(args.ip, args.port)]
else:
    results = ScanRange(args.ip, args.range)
    
if args.sv:
    sortedResults = sorted([r for r in results if r[1]])
    if not args.name: outputName = datetime.now().strftime("%d%m%y_%H%M%S")
    else: outputName = args.name
    with open(f"{outputName}.txt", "w") as f:
        for port, _ in sortedResults:
            try: service = socket.getservbyport(port)
            except OSError:
                service = "Unknown service"
            f.write(f"Port {port} ({service}) on {args.ip} is OPEN\n")