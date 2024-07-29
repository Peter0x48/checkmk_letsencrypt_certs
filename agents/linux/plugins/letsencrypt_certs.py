#!/usr/bin/python3
import subprocess
import re

cert_name_pat = re.compile(r'\s*Certificate Name:\s(\S+)')
cert_expire_date_valid = re.compile(r'\s*Expiry Date:\s\S+\s\S+\s\(VALID:\s(\d+)\s\S+\)')
cert_expire_date_invalid = re.compile(r'\s*Expiry Date:\s\S+\s\S+\s\(INVALID:\s\S+\)')


def get_cert_expiries() -> map:
    proc = subprocess.Popen(["certbot", "certificates"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)
    result = proc.stdout.read()
    result = result.split('\n')
    current_cert = None
    cert_expiries = {}
    for line in result:
        cert_name_match = cert_name_pat.match(line)
        if cert_name_match:
            current_cert = cert_name_match.group(1)
            continue

        cert_expire_date_valid_match = cert_expire_date_valid.match(line)
        if cert_expire_date_valid_match:
            if not current_cert:
                raise Exception('No current certificate name for date match')

            cert_expiries[current_cert] = cert_expire_date_valid_match.group(1)
            current_cert = None
            continue

        cert_expire_date_invalid_match = cert_expire_date_invalid.match(line)
        if cert_expire_date_invalid_match:
            if not current_cert:
                raise Exception('No current certificate name for date match')

            cert_expiries[current_cert] = '0'
            current_cert = None
            continue

    return cert_expiries


print("<<<letsencrypt_certs:sep(59)>>>")
for cert, expiry in get_cert_expiries().items():
    print(f'{cert};{expiry}')
