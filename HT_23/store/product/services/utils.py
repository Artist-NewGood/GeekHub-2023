from django.contrib import messages


def checking_access_rights(request):
    if (not request.user.is_superuser) or (not request.user.is_superuser):
        messages.error(request, "Функція недоступна для звичайного або незалогіненого користувача.")
        return True
    return False
