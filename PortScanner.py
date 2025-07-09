import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="Simple Port Scanner")
parser.add_argument('--ip', required=False, default='192.168.1.254', help='IP address to scan (default: 192.168.1.254)')
parser.add_argument('--port', type=int, required=False, help='Specify a specific port to scan')
parser.add_argument('--range', required=False, default='1-200', help='Specify range to scan (default: 1-200)')
#to add: output file, ouput mode (print/save only open, closed, both)
args = parser.parse_args()

def ScanPort(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    
    if result == 0:
        print(f"Port {port} on {ip} is OPEN")
    else:
        print(f"Port {port} on {ip} is CLOSED")
        
def ScanRange(ip, inputRange):
    minRange, maxRange = map(int, inputRange.split('-'))
    portList = list(range(minRange, maxRange + 1))
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda port: ScanPort(ip, port), portList)    

if args.port:
    ScanPort(args.ip, args.port)              
else:
    ScanRange(args.ip, args.range)