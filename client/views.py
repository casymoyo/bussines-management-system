import datetime
from client.forms import *
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from transactions.models import Transaction
from vouchers.models import voucherTransaction
from transactions.forms import TransactionForm
from client.models import Client, Account, WorkStation
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


# pdf
from config.utils import render_to_pdf


@login_required(login_url="/accounts/login")
def ClientsListView(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    clients = Client.objects.filter(Q(member_status=q) | Q(name__icontains=q))

    return render(
        request,
        "clients/client_list.html",
        {"clients": clients or Client.objects.all()},
    )


@login_required(login_url="/accounts/login")
def ClientsDetailView(request, pk):
    cl = get_object_or_404(Client=pk)
    transactions = Account.objects.filter(client=cl)
    return render(
        request,
        "clients/client_detail.html",
        {"client": cl, "transactions": transactions},
    )

# non permanent client
@login_required(login_url="/accounts/login")
def ClientCreateView(request):
    if request.method == "POST":
        # Validation for client existance
        if Client.objects.filter(phonenumber=request.POST["phonenumber"]).exists():
            return JsonResponse({
                'warning':'Client already exists'
            })
        client = Client(
            user = request.user,
            name = request.POST['name'],
            phonenumber = request.POST['phonenumber'],
            member_status = 'non permanent'
        )
        client.save()
        return JsonResponse({
            'success':'Client created successfully'
        })
    return JsonResponse({
        'error':'failed creating a client'
    })

# permanent client
@login_required(login_url="/accounts/login")
def PermanentCreateView(request):
    if request.method == "POST":
        station = get_object_or_404(WorkStation, id = request.POST['station'])
        # Validation for client existance
        if Client.objects.filter(phonenumber=request.POST["phonenumber"]).exists():
            return JsonResponse({
                'warning':'Client already exists'
            })
        print(request.POST['station'])
        # create new permanent client object
        client = Client(
            user = request.user,
            name = request.POST['name'],
            phonenumber = request.POST['phonenumber'],
            address = request.POST['address'],
            id_number = request.POST['id_number'],
            station_number = station,
            member_status = 'permanent'
        )
        client.save()
        # update the workstation status
        station.status = 'occupied'
        station.save()
        return JsonResponse({
            'success':'Client created successfully'
        })
    return JsonResponse({
        'error':'failed creating a client'
    })

@login_required(login_url="/accounts/login")
def UpdatePermnent(request, pk):
    cl = get_object_or_404(Client, id=pk)
    form = ClientMememberForm(instance=cl or None)
    if request.POST['name'] == '' or request.POST['phonenumber'] == '':
        messages.warning(request, 'Please check name or phone field(s), cant be empty ')
        return redirect('client:clients')
    if form.is_valid():
        form.save()
        messages.success(request, f"client successfully updated")
        return redirect('client:clients')
    return render(
        request, "clients/createClient.html", {"form": form, "client": cl}
    )
        

@login_required(login_url="/accounts/login")
def UpdateNonPermenent(request, pk):
    cl = get_object_or_404(Client, id=pk)
    form = ClientDayForm(instance=cl or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f"client successfully updated")    
            return redirect('client:clients')
        print('FAILED')
    return render(
        request, "clients/createClient.html", {"form": form, "client": cl}
    )

@login_required(login_url="/accounts/login")
def clientCancellatioin(request, pk):
    cl = get_object_or_404(Client=pk)
    return render(request, "client/cancleClient.html")

# renders the pos html
@login_required(login_url="/accounts/login")
def Pos(request):
    return render(
        request,
        "pos.html",
        {
            "clients": Client.objects.all(), "account": Account.objects.all(),
            'stations': WorkStation.objects.filter(status = 'vaccant'),
            'vouchers' : voucherTransaction.objects.all(),
            'desks' : Transaction.objects.filter(status = 'day'),
            'form':TransactionForm()
        },
    )
    

@login_required(login_url="/accounts/login")
def posData(request):
    clients = Client.objects.all()
    return JsonResponse({
        'clients': list(clients.values())
    })


@login_required(login_url="/accounts/login")
def clientPdfGenerator(request):
    template_name = "reports/clientsPdf.html"
    clients = Client.objects.all()
    return render_to_pdf(
        template_name,
        {
            "clients": clients,
            'date': datetime.date.today()
        },
    )
   
# provide data to django-select2  
@login_required(login_url="/accounts/login")
def clientData(request):
    clients = Client.objects.all()
    json_data = []
    for client in clients:
        json_data.append({"id": client.id, "text": client.name})

    return JsonResponse(json_data, safe=False)

