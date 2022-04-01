from django.shortcuts import render


def private_policies(request):
    """

    """
    return render(request, 'root/privacy_policy.html')


def terms_of_use(request):
    """

    """
    return render(request, 'root/terms_of_use.html')