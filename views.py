from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import User, Rent, UtilityEntry, DebtEntry, Entry
from .util import decimal_truncate, decimal_make, RentsplitterError

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
            users[util.payer.name] -= util.amount
        split = pool / len(users)
        for u in users:
            users[u] += split
        for debt in debts:
            users[debt.payer.name] += debt.amount
            users[debt.payee.name] -= debt.amount
        subtotal = decimal_make(0, prec=2)
        for u in users:
            users[u] = decimal_truncate(users[u], prec=2)
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
    try:
        amt = decimal_make(request.POST['amount'], prec=2)
        note = request.POST['note']
        if not note:
            raise RentsplitterError('Note cannot be empty')
        try:
            payer = User.objects.get(name=request.POST['payer'])
        except:
            raise RentsplitterError('Payer does not exist')
        if request.POST['type'] == 'utility':
            e = UtilityEntry(amount=amt, payer=payer, note=note)
            e.save()
        elif request.POST['type'] == 'debt':
            try:
                payee = User.objects.get(name=request.POST['payee'])
            except:
                raise RentsplitterError('Payee does not exist')
            if payer.name == payee.name:
                raise RentsplitterError('Payer and payee cannot be the same')
            e = DebtEntry(amount=amt, payer=payer, payee=payee, note=note)
            e.save()
        else:
            raise RentsplitterError('Invalid type')
        return JsonResponse({})
    except KeyError:
        return JsonResponse({'error': 'Missing parameter'})
    except RentsplitterError as e:
        return JsonResponse({'error': e.msg})

@require_POST
def delete(request):
    try:
        entry = Entry.objects.get(pk=request.POST['id'])
        entry.delete()
        return JsonResponse({})
    except KeyError:
        return JsonResponse({'error': 'Missing parameter'})
    except Entry.DoesNotExist:
        return JsonResponse({'error': 'Expense does not exist'})
