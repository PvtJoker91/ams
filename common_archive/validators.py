import re


def validate_ab_barcode(barcode):
    pattern = r'AB/\d{2}-\d{6}'
    return re.match(pattern, barcode)



def validate_dossier_barcode(barcode):
    pattern = r'D\d{2}-\d{2}-\d{8}|d{5}-d{5}-d{5}-d{5}-d{5}|d{25}'
    return re.match(pattern, barcode)
