#!/usr/bin/env python3
"""
Simple ICAP Server with ClamAV integration
Handles REQMOD/RESPMOD requests and scans files with ClamAV
"""

__version__ = "1.2.1"
__author__ = "Roland Imme"

import socket
import socketserver
import threading
import logging
import argparse
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('icap-server')


class ClamAVClient:
    """Client for communicating with ClamAV daemon"""
    
    def __init__(self, host: str = 'clamav', port: int = 3310):
        self.host = host
        self.port = port
    
    def scan_bytes(self, data: bytes) -> Tuple[bool, str]:
        """
        Scan bytes with ClamAV
        
        Returns:
            Tuple of (is_infected, virus_name)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.host, self.port))
            
            # Send INSTREAM command
            sock.sendall(b'zINSTREAM\0')
            
            # Send data in chunks
            chunk_size = 4096
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                size = len(chunk)
                # Send chunk size (4 bytes, network byte order) + chunk
                sock.sendall(size.to_bytes(4, 'big') + chunk)
            
            # Send zero-length chunk to signal end
            sock.sendall(b'\x00\x00\x00\x00')
            
            # Receive response
            response = sock.recv(4096).decode('utf-8', errors='ignore')
            sock.close()
            
            logger.debug(f"ClamAV response: {response}")
            
            # Parse response
            if 'FOUND' in response:
                virus_name = response.split(':')[1].strip().replace(' FOUND', '')
                return True, virus_name
            elif 'OK' in response:
                return False, 'Clean'
            else:
                logger.warning(f"Unexpected ClamAV response: {response}")
                return False, 'Unknown'
                
        except Exception as e:
            logger.error(f"Error scanning with ClamAV: {e}")
            return False, f'Error: {str(e)}'
    
    def ping(self) -> bool:
        """Check if ClamAV is reachable"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.host, self.port))
            sock.sendall(b'zPING\0')
            response = sock.recv(1024)
            sock.close()
            return b'PONG' in response
        except Exception as e:
            logger.error(f"ClamAV ping failed: {e}")
            return False


class ICAPRequestHandler(socketserver.StreamRequestHandler):
    """Handler for ICAP requests"""
    
    def __init__(self, *args, **kwargs):
        self.clamav = ClamAVClient()
        super().__init__(*args, **kwargs)
    
    def handle(self):
        """Handle incoming ICAP request"""
        try:
            # Read request line
            request_line = self.rfile.readline().decode('utf-8', errors='ignore').strip()
            logger.info(f"Request: {request_line}")
            
            if not request_line:
                return
            
            parts = request_line.split()
            if len(parts) < 3:
                self.send_error(400, "Bad Request")
                return
            
            method = parts[0]
            
            if method == 'OPTIONS':
                self.handle_options()
            elif method == 'REQMOD':
                self.handle_reqmod()
            elif method == 'RESPMOD':
                self.handle_respmod()
            else:
                self.send_error(405, "Method Not Allowed")
        
        except Exception as e:
            logger.error(f"Error handling request: {e}", exc_info=True)
            self.send_error(500, "Internal Server Error")
    
    def handle_options(self):
        """Handle OPTIONS request"""
        response = (
            "ICAP/1.0 200 OK\r\n"
            "Methods: REQMOD, RESPMOD\r\n"
            "Service: Python ICAP Server with ClamAV\r\n"
            "ISTag: \"python-icap-1.0\"\r\n"
            "Encapsulated: null-body=0\r\n"
            "Max-Connections: 100\r\n"
            "Options-TTL: 3600\r\n"
            "Preview: 0\r\n"
            "\r\n"
        )
        self.wfile.write(response.encode('utf-8'))
        logger.info("Sent OPTIONS response")
    
    def handle_reqmod(self):
        """Handle REQMOD request (request modification)"""
        self.handle_scan_request()
    
    def handle_respmod(self):
        """Handle RESPMOD request (response modification)"""
        self.handle_scan_request()
    
    def handle_scan_request(self):
        """Common handler for scan requests"""
        headers = {}
        body_data = b''
        
        # Read ICAP headers
        while True:
            line = self.rfile.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        logger.debug(f"ICAP Headers: {headers}")
        
        # Read HTTP headers (encapsulated)
        http_headers = {}
        while True:
            line = self.rfile.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                break
            if ':' in line:
                key, value = line.split(':', 1)
                http_headers[key.strip().lower()] = value.strip()
        
        logger.debug(f"HTTP Headers: {http_headers}")
        
        # Read body (chunked encoding)
        try:
            while True:
                chunk_size_line = self.rfile.readline().decode('utf-8', errors='ignore').strip()
                if not chunk_size_line:
                    break
                
                # Parse chunk size (hex)
                try:
                    chunk_size = int(chunk_size_line, 16)
                except ValueError:
                    logger.warning(f"Invalid chunk size: {chunk_size_line}")
                    break
                
                if chunk_size == 0:
                    break
                
                # Read chunk data
                chunk = self.rfile.read(chunk_size)
                body_data += chunk
                
                # Read trailing CRLF
                self.rfile.readline()
        except Exception as e:
            logger.warning(f"Error reading body: {e}")
        
        logger.info(f"Received {len(body_data)} bytes to scan")
        
        # Scan with ClamAV
        is_infected, result = self.clamav.scan_bytes(body_data)
        
        if is_infected:
            logger.warning(f"THREAT DETECTED: {result}")
            self.send_threat_response(result)
        else:
            logger.info(f"File clean: {result}")
            self.send_clean_response()
    
    def send_clean_response(self):
        """Send response for clean file"""
        response = (
            "ICAP/1.0 204 No Modifications Needed\r\n"
            "ISTag: \"python-icap-1.0\"\r\n"
            "Date: Thu, 01 Jan 2026 00:00:00 GMT\r\n"
            "\r\n"
        )
        self.wfile.write(response.encode('utf-8'))
    
    def send_threat_response(self, virus_name: str):
        """Send response for infected file"""
        response = (
            f"ICAP/1.0 403 Forbidden\r\n"
            f"ISTag: \"python-icap-1.0\"\r\n"
            f"X-Violations-Found: 1\r\n"
            f"X-Virus-ID: {virus_name}\r\n"
            f"Encapsulated: res-hdr=0, res-body=0\r\n"
            f"\r\n"
        )
        self.wfile.write(response.encode('utf-8'))
    
    def send_error(self, code: int, message: str):
        """Send ICAP error response"""
        response = (
            f"ICAP/1.0 {code} {message}\r\n"
            f"ISTag: \"python-icap-1.0\"\r\n"
            f"Encapsulated: null-body=0\r\n"
            f"\r\n"
        )
        self.wfile.write(response.encode('utf-8'))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Multi-threaded TCP server"""
    allow_reuse_address = True
    daemon_threads = True


def main():
    """Start ICAP server"""
    parser = argparse.ArgumentParser(
        description='ICAP Server with ClamAV integration'
    )
    parser.add_argument('--version', action='version', 
                        version=f'%(prog)s {__version__}')
    parser.add_argument('--author', action='store_true',
                        help='Show author information')
    parser.add_argument('--host', default='0.0.0.0',
                        help='Server host (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=1344,
                        help='Server port (default: 1344)')
    
    args = parser.parse_args()
    
    if args.author:
        logger.info(f"ICAP Server")
        logger.info(f"Version: {__version__}")
        logger.info(f"Author: {__author__}")
        return
    
    host = args.host
    port = args.port
    
    # Test ClamAV connection
    clamav = ClamAVClient()
    logger.info("Testing ClamAV connection...")
    if clamav.ping():
        logger.info("✓ ClamAV connection successful")
    else:
        logger.error("✗ ClamAV connection failed - server will start anyway")
    
    # Start server
    server = ThreadedTCPServer((host, port), ICAPRequestHandler)
    logger.info(f"ICAP Server started on {host}:{port}")
    logger.info("Ready to handle requests...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.shutdown()
        logger.info("Server stopped")


if __name__ == '__main__':
    main()
