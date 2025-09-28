import re
import phonenumbers
import logging

log = logging.getLogger(__name__)

def normalized_phone(phone: str, default_region: str = "US") -> str:
    digits = re.sub(r"[^\d\+]", "", phone)
    try:
        parsed = phonenumbers.parse(digits, default_region)
        if not phonenumbers.is_valid_number(parsed):
            return None
        return phonenumbers.format_numbers(parsed, phonenumbers.PhoneNumberFormat.E164)
    except Exception as e:
        log.debug("Phone Numbers parse failed: %s", e)
        return None