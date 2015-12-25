from decimal import Decimal, ROUND_DOWN

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import User, Rent, UtilityEntry, DebtEntry

def index(request):
    base_rent = Rent.objects.first().amount
    pool = base_rent
    users = {user.name: 0 for user in User.objects.all()}
    utilities = list(UtilityEntry.objects.all())
    debts = list(DebtEntry.objects.all())
    entries = sorted(utilities + debts, key=lambda e: e.date)
    if users:
        for util in utilities:
            pool += util.amount
            users[util.payer] -= util.amount
        split = pool / len(users)
        for u in users:
            users[u] += split
        for debt in debts:
            users[debt.payer.name] += debt.amount
            users[debt.payee.name] -= debt.amount
        subtotal = Decimal(0)
        for u in users:
            users[u] = users[u].quantize(Decimal('.01'), rounding=ROUND_DOWN)
            subtotal += users[u]
        users[users.keys()[0]] += base_rent - subtotal
    context = {
        'base_rent': base_rent,
        'total_pool': pool,
        'users': users,
        'entries': entries,
    }
    return render(request, 'rentsplitter/index.html', context=context)

@require_POST
def expense(request):
    return JsonResponse({'yay': True})
