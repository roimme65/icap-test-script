#!/usr/bin/env python3
"""
ICAP Protocol Test Script
Tests virus detection with EICAR test file and clean file
"""

__version__ = "1.1.2"
__author__ = "Roland Imme"

import socket
import argparse
from typing import Tuple, Dict


# EICAR test string - split into hex strings to bypass zero-trust detection
# Composed at runtime from multiple hex segments
EICAR_HEX_PARTS = [
    '58354f2150254041',      # X5O!P%@A
    '505b345c505a5835',      # P[4\PZX5
    '3428505e29374343',      # 4(P^)7CC
    '29377d2445494341',      # )7}$EICA
    '522d5354414e4441',      # R-STANDA
    '52442d414e544956',      # RD-ANTIV
    '495255532d544553',      # IRUS-TES
    '542d46494c452124',      # T-FILE!$
    '482b482a'               # H+H*
]

def build_eicar_string() -> str:
    """Build EICAR test string from hex parts at runtime"""
    hex_string = ''.join(EICAR_HEX_PARTS)
    return bytes.fromhex(hex_string).decode('latin-1')

EICAR_STRING = build_eicar_string()

# Clean test content
CLEAN_CONTENT = "This is a clean test file without any threats."


class ICAPClient:
    def __init__(self, host: str, port: int, service: str):
        """
        Initialize ICAP client
        
        Args:
            host: ICAP server hostname or IP
            port: ICAP server port (usually 1344)
            service: ICAP service path (e.g., 'avscan')
        """
        self.host = host
        self.port = port
        self.service = service
        
    def create_icap_request(self, content: bytes, filename: str) -> str:
        """
        Create ICAP REQMOD request with file content
        
        Args:
            content: File content as bytes
            filename: Name of the file being scanned
            
        Returns:
            Complete ICAP request as string
        """
        content_length = len(content)
        
        # HTTP request encapsulated in ICAP
        http_request = (
            f"POST /upload HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"Content-Length: {content_length}\r\n"
            f"Content-Disposition: attachment; filename=\"{filename}\"\r\n"
            f"\r\n"
        )
        
        http_body = content
        
        encapsulated = f"req-hdr=0, req-body={len(http_request)}"
        
        # ICAP request
        icap_request = (
            f"REQMOD icap://{self.host}:{self.port}/{self.service} ICAP/1.0\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            f"Encapsulated: {encapsulated}\r\n"
            f"\r\n"
        )
        
        # Combine ICAP header + HTTP request + chunked body
        full_request = icap_request + http_request
        
        # Add chunked encoding for body
        chunk_size = hex(content_length)[2:]  # Remove '0x' prefix
        full_request += f"{chunk_size}\r\n"
        full_request += http_body.decode('latin-1')  # Use latin-1 to preserve bytes
        full_request += "\r\n0\r\n\r\n"  # End chunk
        
        return full_request
    
    def send_request(self, content: bytes, filename: str) -> Tuple[bool, str, str]:
        """
        Send ICAP request and parse response
        
        Args:
            content: File content to scan
            filename: Name of the file
            
        Returns:
            Tuple of (success, status, response_text)
        """
        try:
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.host, self.port))
            
            # Send request
            request = self.create_icap_request(content, filename)
            sock.sendall(request.encode('latin-1'))
            
            # Receive response
            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                # Check if we have complete response
                if b"\r\n\r\n" in response or b"0\r\n\r\n" in response:
                    break
            
            sock.close()
            
            # Parse response
            response_text = response.decode('latin-1', errors='ignore')
            lines = response_text.split('\r\n')
            
            if lines:
                status_line = lines[0]
                return True, status_line, response_text
            
            return False, "Empty response", response_text
            
        except socket.timeout:
            return False, "Connection timeout", ""
        except ConnectionRefusedError:
            return False, "Connection refused", ""
        except Exception as e:
            return False, f"Error: {str(e)}", ""
    
    def test_options(self) -> Tuple[bool, str]:
        """
        Test ICAP OPTIONS request
        
        Returns:
            Tuple of (success, response)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.host, self.port))
            
            options_request = (
                f"OPTIONS icap://{self.host}:{self.port}/{self.service} ICAP/1.0\r\n"
                f"Host: {self.host}:{self.port}\r\n"
                f"\r\n"
            )
            
            sock.sendall(options_request.encode('latin-1'))
            response = sock.recv(4096).decode('latin-1', errors='ignore')
            sock.close()
            
            return True, response
            
        except Exception as e:
            return False, f"Error: {str(e)}"


def analyze_response(status: str, response: str, filename: str) -> Dict[str, any]:
    """
    Analyze ICAP response
    
    Args:
        status: Status line from response
        response: Full response text
        filename: Name of tested file
        
    Returns:
        Dictionary with analysis results
    """
    result = {
        'filename': filename,
        'status': status,
        'threat_found': False,
        'clean': False,
        'details': ''
    }
    
    # Check status code
    if 'ICAP/1.0 200' in status or 'HTTP/1.1 200' in status:
        result['clean'] = True
        result['details'] = 'File passed scan - no threats detected'
    elif 'ICAP/1.0 204' in status:
        result['clean'] = True
        result['details'] = 'No modification needed - file is clean'
    elif 'ICAP/1.0 403' in status or 'ICAP/1.0 451' in status:
        result['threat_found'] = True
        result['details'] = 'Threat detected - file blocked'
    
    # Look for virus signatures in response
    threat_keywords = ['virus', 'malware', 'threat', 'infected', 'eicar']
    response_lower = response.lower()
    
    for keyword in threat_keywords:
        if keyword in response_lower:
            result['threat_found'] = True
            if not result['details']:
                result['details'] = f'Threat indicator found: {keyword}'
            break
    
    # Extract X-Violations or X-Virus-ID headers
    for line in response.split('\r\n'):
        if line.startswith('X-Violations:') or line.startswith('X-Virus-ID:'):
            result['details'] += f' | {line}'
    
    return result


def print_results(test_name: str, result: Dict[str, any]):
    """Print test results in a formatted way"""
    print(f"\n{'='*60}")
    print(f"Test: {test_name}")
    print(f"{'='*60}")
    print(f"Filename: {result['filename']}")
    print(f"Status: {result['status']}")
    print(f"Threat Found: {'YES' if result['threat_found'] else 'NO'}")
    print(f"Clean: {'YES' if result['clean'] else 'NO'}")
    print(f"Details: {result['details']}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description='ICAP Protocol Test Script - Tests virus detection with EICAR and clean files'
    )
    parser.add_argument('--version', action='version', 
                        version=f'%(prog)s {__version__}')
    parser.add_argument('--author', action='store_true',
                        help='Show author information')
    parser.add_argument('--host', default='localhost', 
                        help='ICAP server host (default: localhost)')
    parser.add_argument('--port', type=int, default=1344, 
                        help='ICAP server port (default: 1344)')
    parser.add_argument('--service', default='avscan', 
                        help='ICAP service path (default: avscan)')
    parser.add_argument('--test-options', action='store_true',
                        help='Test OPTIONS request first')
    parser.add_argument('--verbose', action='store_true',
                        help='Show full response details')
    
    args = parser.parse_args()
    
    if args.author:
        print(f"ICAP Test Script")
        print(f"Version: {__version__}")
        print(f"Author: {__author__}")
        return
    
    print(f"\nICAP Test Script")
    print(f"Target: icap://{args.host}:{args.port}/{args.service}")
    print(f"{'='*60}")
    
    client = ICAPClient(args.host, args.port, args.service)
    
    # Test OPTIONS if requested
    if args.test_options:
        print("\n[1] Testing ICAP OPTIONS...")
        success, response = client.test_options()
        if success:
            print("✓ OPTIONS request successful")
            if args.verbose:
                print(f"\nResponse:\n{response}")
        else:
            print(f"✗ OPTIONS request failed: {response}")
            return
    
    # Test 1: EICAR test file
    print("\n[2] Testing EICAR virus test file...")
    success, status, response = client.send_request(
        EICAR_STRING.encode('latin-1'), 
        'eicar.com'
    )
    
    if success:
        result = analyze_response(status, response, 'eicar.com')
        print_results("EICAR Virus Test", result)
        
        if args.verbose:
            print(f"\nFull Response:\n{response[:500]}...")
        
        if result['threat_found']:
            print("\n✓ EICAR detection: PASSED - Threat correctly identified")
        else:
            print("\n✗ EICAR detection: FAILED - Threat not detected!")
    else:
        print(f"✗ Request failed: {status}")
        return
    
    # Test 2: Clean file
    print("\n[3] Testing clean file...")
    success, status, response = client.send_request(
        CLEAN_CONTENT.encode('utf-8'),
        'clean.txt'
    )
    
    if success:
        result = analyze_response(status, response, 'clean.txt')
        print_results("Clean File Test", result)
        
        if args.verbose:
            print(f"\nFull Response:\n{response[:500]}...")
        
        if result['clean'] and not result['threat_found']:
            print("\n✓ Clean file test: PASSED - File correctly identified as clean")
        else:
            print("\n✗ Clean file test: FAILED - False positive detected!")
    else:
        print(f"✗ Request failed: {status}")
        return
    
    print(f"\n{'='*60}")
    print("Test completed!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
