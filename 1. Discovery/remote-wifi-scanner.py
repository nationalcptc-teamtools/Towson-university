//
//
//  Post exploitation script to scan wifi networks surrounding the exploited controller
//
//  by. Danno

import paramiko
import argparse

# Define command-line arguments
parser = argparse.ArgumentParser(description="Remote Wi-Fi SSID Scanner")
parser.add_argument("--host", required=True, help="Remote controller IP address")
parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22)")
parser.add_argument("--username", required=True, help="SSH username")
parser.add_argument("--password", help="SSH password")
parser.add_argument("--private-key", help="Path to the private key file for key-based authentication")
args = parser.parse_args()

# Use command-line arguments
ssh_host = args.host
ssh_port = args.port
ssh_username = args.username
ssh_password = args.password
private_key_path = args.private_key

# Define the command to run for Wi-Fi SSID scan
ssid_scan_command = 'iwlist wlan0 scan | grep ESSID'

try:
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()

    # Automatically add the server's host key
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if private_key_path:
        # Authenticate using a private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        ssh_client.connect(ssh_host, ssh_port, ssh_username, pkey=private_key)
    else:
        # Authenticate using a password
        if not ssh_password:
            raise ValueError("You must provide either a password or a private key for authentication.")
        ssh_client.connect(ssh_host, ssh_port, ssh_username, ssh_password)

    # Execute the remote Wi-Fi SSID scan command
    stdin, stdout, stderr = ssh_client.exec_command(ssid_scan_command)

    output = stdout.read().decode('utf-8')
    print("Wi-Fi SSID Scan Results:")
    print(output)

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    ssh_client.close()
