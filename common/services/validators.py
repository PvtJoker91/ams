import re

from rest_framework.exceptions import ParseError


def validate_ab_barcode(barcode: str) -> bool:
    pattern = r'AB-\d{2}-\d{6}$'
    if not re.match(pattern, barcode):
        raise ParseError('Wrong barcode format')
    return True


def validate_dossier_barcode(barcode: str) -> bool:
    pattern = r'D\d{2}-\d{2}-\d{8}$|d{5}-d{5}-d{5}-d{5}-d{5}$|d{25}$'
    if not re.match(pattern, barcode):
        raise ParseError('Wrong barcode format')
    return True
