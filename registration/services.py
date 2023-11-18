from bank_clients.models import Contract


def register_dossier(**kwargs):
    contract = Contract.objects.filter(**kwargs)
