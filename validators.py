import ipaddress


def validate_ip(ip: str) -> str:
    try:
        return str(ipaddress.ip_address(ip))
    except ValueError:
        raise ValueError(f"Invalid IP address: {ip}")