import logging
from ssl import SSLContext
from typing import Optional

from .dns_check import dns_check, DefaultAddressTypes, AddressTypes
from .domainlist_check import domainlist_check
from .email_address import EmailAddress
from .exceptions import (
    AddressFormatError, EmailValidationError, FromAddressFormatError,
    SMTPTemporaryError)
from .regex_check import regex_check
from .smtp_check import smtp_check

LOGGER = logging.getLogger(name=__name__)
logging.basicConfig(level=logging.DEBUG)

__all__ = ['validate_email', 'validate_email_or_fail']

def validate_email_or_fail(
    email_address: str, *, check_format: bool = True,
    check_blacklist: bool = False, check_dns: bool = False,
    dns_timeout: float = 10, check_smtp: bool = True,
    smtp_timeout: float = 10, smtp_helo_host: Optional[str] = None,
    smtp_from_address: Optional[str] = None,
    smtp_skip_tls: bool = False, smtp_tls_context: Optional[SSLContext] = None,
    smtp_debug: bool = False, address_types: AddressTypes = DefaultAddressTypes
) -> Optional[bool]:
    """
    Return `True` if the email address validation is successful, `None`
    if the validation result is ambiguous, and raise an exception if the
    validation fails.
    """
    LOGGER.debug(f"Validating email: {email_address}")
    
    email_address_to = EmailAddress(address=email_address)
    
    if check_format:
        LOGGER.debug("Checking email format...")
        regex_check(email_address=email_address_to)
    
    if check_blacklist:
        LOGGER.debug("Checking blacklist...")
        domainlist_check(email_address=email_address_to)
    
    if not check_dns and not check_smtp:
        LOGGER.debug("Skipping DNS and SMTP checks. Returning True.")
        return True
    
    LOGGER.debug("Checking DNS records...")
    mx_records = dns_check(
        email_address=email_address_to, timeout=dns_timeout,
        address_types=address_types)
    LOGGER.debug(f"MX Records found: {mx_records}")
    
    if not check_smtp:
        LOGGER.debug("Skipping SMTP check. Returning True.")
        return True
    
    try:
        email_address_from = None if not smtp_from_address else EmailAddress(address=smtp_from_address)
    except AddressFormatError:
        raise FromAddressFormatError
    
    LOGGER.debug("Performing SMTP check...")
    result = smtp_check(
        email_address=email_address_to, mx_records=mx_records,
        timeout=smtp_timeout, helo_host=smtp_helo_host,
        from_address=email_address_from, skip_tls=smtp_skip_tls,
        tls_context=smtp_tls_context, debug=smtp_debug)
    
    LOGGER.debug(f"SMTP Check result: {result}")
    return result

def validate_email(email_address: str, **kwargs):
    """
    Return `True` or `False` depending if the email address exists
    or/and can be delivered.

    Return `None` if the result is ambiguous.
    """
    try:
        return validate_email_or_fail(email_address, **kwargs)
    except SMTPTemporaryError as error:
        LOGGER.info(f'Validation for {email_address!r} is ambiguous: {error}')
        return None
    except EmailValidationError as error:
        LOGGER.info(f'Validation for {email_address!r} failed: {error}')
        return False
