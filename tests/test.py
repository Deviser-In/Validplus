import sys
import os
import ssl
import socket
import random
import socks
import requests
from ipaddress import IPv4Address, IPv6Address
from validate_email import validate_email

# Example proxy pool (replace with actual proxies)
proxy_pool = [
    "123.456.789.101:8080",  # Format: "ip:port"
    "234.567.890.123:3128",
    "345.678.901.234:8000"
]

# Randomly choose a proxy from the pool
random_proxy = random.choice(proxy_pool)

# Use the chosen proxy with SOCKS5
proxy_ip, proxy_port = random_proxy.split(":")
proxy_port = int(proxy_port)

# Create SSL context
context = ssl.create_default_context()

# Email address to validate
email = "vartikkanand@gmail.com"

# Use the SOCKS proxy for all requests (not just SMTP)
socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
socket.socket = socks.socksocket  # This overrides the default socket to use the proxy

# Validate email with increased timeouts
isValidEmail = validate_email(
    email_address=email,
    check_format=True,
    check_blacklist=False,
    check_dns=True,
    dns_timeout=40,  # Increased DNS timeout
    check_smtp=True,
    smtp_timeout=40,  # Increased SMTP timeout
    smtp_helo_host=None,
    smtp_from_address=None,
    smtp_skip_tls=True,
    smtp_tls_context=context,
    smtp_debug=True,
    address_types=frozenset([IPv4Address, IPv6Address])
)

# Handle the result of validation
if isValidEmail is True:
    print(f"{email} is a valid email.")
else:
    print(f"{email} is an invalid email.")
