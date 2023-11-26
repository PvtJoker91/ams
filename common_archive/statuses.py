AB_STATUSES = (None, 'Under registration', 'Is registered',
               'Under completion', 'Is completed',
               'Under checking', 'Is checked',
               'Under storage', 'Removed from storage',
               'Checked with a error')
AB_REGISTRATION_AVAILABLE_STATUSES = (
    None, 'Under registration', 'Is registered', 'Checked with a error', 'Checked with a error')
AB_COMPLETION_AVAILABLE_STATUSES = (
    None, 'Under completion', 'Is completed', 'Under storage', 'Removed from storage', 'Is checked')
AB_CHECKING_AVAILABLE_STATUSES = (
    None, 'Is registered', 'Is completed', 'Under storage', 'Removed from storage', 'Is checked', 'Under checking',
    'Checked with a error')
AB_PLACEMENT_AVAILABLE_STATUSES = (None, 'Is registered', 'Is completed', 'Removed from storage', 'Is checked')

DOSSIER_STATUSES = (None, 'Under registration', 'Is registered',
                    'Under completion', 'Is completed',
                    'Under checking', 'Is checked',
                    'Under storage', 'Removed from storage',
                    'Checked with a error',
                    'Removed from a box', 'Added to a box',
                    'Checked in a box',
                    'Not found while checking', 'Wrong operation/sector')
DOSSIER_REGISTRATION_AVAILABLE_STATUSES = ('Is registered',)
DOSSIER_COMPLETION_AVAILABLE_STATUSES = (
    None, 'Under completion', 'Is completed', 'Removed from storage', 'Is checked', 'Removed from a box',
    'Added to a box', 'Not found while checking', 'Checked with a error')
DOSSIER_CHECKING_AVAILABLE_STATUSES = (
    None, 'Is completed', 'Removed from storage', 'Is checked', 'Under checking', 'Checked in a box',
    'Removed from a box', 'Not found while checking', 'Checked with a error')
