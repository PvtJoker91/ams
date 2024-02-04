import re

from rest_framework.exceptions import ParseError

from archive.models import Dossier


def validate_ab_barcode(barcode: str) -> bool:
    pattern = r'AB-\d{2}-\d{6}$'
    if not re.match(pattern, barcode):
        raise ParseError('Неверный формат штрих-кода')
    return True


def validate_dossier_barcode(barcode: str) -> bool:
    pattern = r'D\d{2}-\d{2}-\d{8}$|d{5}-d{5}-d{5}-d{5}-d{5}$|d{25}$'
    if not re.match(pattern, barcode):
        raise ParseError('Неверный формат штрих-кода')
    return True


def validate_dossier_status(instance: Dossier, available_statuses: tuple) -> bool:
    if instance.status not in available_statuses:
        raise ParseError(f"Досье не должно находиться на данной операции. Текущий статус досье - {instance.status}")
    return True
