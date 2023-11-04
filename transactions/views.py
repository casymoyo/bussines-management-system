from datetime import date
import moneyed
from . import forms, models
from django.db.models import Q, Sum
from django.contrib import messages
from django.http import JsonResponse
from config.utils import render_to_pdf
from datetime import datetime, timedelta
from client.models import Client, WorkStation
from vouchers.models import vouchers, voucherTransaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404


@login_required(login_url="/accounts/login")
def transactions(request):

    trans = request.GET.get('q') if request.GET.get('q') is not None else models.Transaction.objects.filter(
        date_created=date.today())
    total_amount = trans.aggregate(Sum('amount'))
    return render(
        request,
        'transactions/transactions.html',
        {
            'transactions': trans,
            'total': total_amount['amount__sum']
        }
    )


@login_required(login_url="/accounts/login")
def TransactioinCreateView(request):
    if request.method == 'POST':
        # get client object and product object
        cl = Client.objects.get(id=request.POST['client'])
        p = models.Product.objects.get(id=request.POST['product'])
        print(p)
        # validate amount
        if int(request.POST['amount']) < 0 or int(request.POST['amount']) == 0:
            return JsonResponse({'warning': 'amount cant be zero or below zero'})
        if str(p) in ['cafe(1)', 'cafe(2)', 'cafe(3)', 'cafe(4)', 'cafe(5)']:
            # product and voucher matching (conditional over cafe products)
            if str(p) == 'cafe(1)':
                vou = vouchers.objects.filter(file__category=1)
                voucher = vou.filter(status='unused').first()
                e_time = datetime.now() + timedelta(minutes=65)  # 1 hour and 5 minutes for preparation
            elif str(p) == 'cafe(2)':
                vou = vouchers.objects.filter(file__category=2)
                voucher = vou.filter(status='unused').first()
                e_time = datetime.now() + timedelta(minutes=125)  # 2 hours and 5 minutes for preparation
            elif str(p) == 'cafe(3)':
                vou = vouchers.objects.filter(file__category=3)
                voucher = vou.filter(status='unused').first()
                e_time = datetime.now() + timedelta(minutes=185)  # 3 hours and 5 minutes for preparation
            elif str(p) == 'cafe(4)':
                vou = vouchers.objects.filter(file__category=4)
                voucher = vou.filter(status='unused').first()
                e_time = datetime.now() + timedelta(minutes=245)  # 4 hours and 5 minutes for preparation
            elif str(p) == 'cafe(5)':
                vou = vouchers.objects.filter(file__category=5)
                voucher = vou.filter(status='unused').first()
                e_time = datetime.now() + timedelta(minutes=300)  # 5 hours and 5 minutes for preparation
            else:
                return JsonResponse({'voucher_message': 'Product doesnt exists'})

                # update the voucher status
            vou_obj = vouchers.objects.get(id=voucher.id)
            vou_obj.status = 'used'

            # create a voucher transaction
            vou_transaction_obj = voucherTransaction(
                vouch=vou_obj,
                client=cl,
                user=request.user,
                start_time=datetime.now(),
                end_time=e_time,
                work_station=WorkStation.objects.get(id=request.POST['station'])
            )

            # create transaction
            day_obj = models.Transaction(
                user=request.user,
                client=cl,
                status='cafe',
                product=p,
                amount=request.POST['amount'],
                work_station=WorkStation.objects.get(id=request.POST['station'])
            )
            day_obj.save()
            vou_obj.save()
            vou_transaction_obj.save()

            # client sale count (if exist)

            if models.Transaction.objects.filter(id=cl.id).exists():
                cl.count += 1
                cl.save()
            else:
                cl.count = 1
                cl.save()
            return JsonResponse({
                'success': 'transaction successfully created'
            })
        elif str(p) in ['premium', 'professional', 'standard']:
            # calculate amount owing
            c = p.price

            if moneyed.Money(request.POST['amount'], 'USD') < p.price:
                owing_amount = p.price - moneyed.Money(request.POST['amount'], 'USD')
            else:
                owing_amount = 0
            # validate if client is permanent
            if cl.station_number is None:
                return JsonResponse({'warning': 'Please update the client to be a permanent member'})
            else:
                monthly_obj = models.Transaction(
                    user=request.user,
                    client=cl,
                    product=p,
                    status='monthly',
                    work_station=WorkStation.objects.get(id=cl.station_number.id),
                    amount=request.POST['amount'],
                    owing=owing_amount
                )
                monthly_obj.save()
                return JsonResponse({
                    'success': 'transaction successfully created'
                })
        else:
            # day desk transaction
            day_obj = models.Transaction(
                user=request.user,
                client=cl,
                product=p,
                status='day',
                amount=request.POST['amount'],
                work_station=WorkStation.objects.get(id=request.POST['station'])
            )
            day_obj.save()
            print('saved')
            return JsonResponse({
                'success': 'transaction successfully created'
            })
    return JsonResponse({
        'failed': 'transaction failed successfully'
    })


@login_required(login_url="/accounts/login")
def Account(request, pk):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    client = get_object_or_404(Client, id=pk)
    trans = models.Transaction.objects.filter(client=client)
    acc_transactions = trans.filter(
        Q(date_created__icontains=q) |
        Q(amount__icontains=q) |
        Q(owing__icontains=q)
    )
    return render(
        request,
        'transactions/account.html',
        {
            'transactions': acc_transactions or trans,
            'client': client
        }
    )

# function for total amount of expenses computation
# worried with performance as the dataset increases :(
def salesTotal(sales_data):
    total_sales = 0
    exp = sales_data.annotate(total=Sum('amount'))
    for exp in exp:
        total_sales = exp.amount + total_sales
    return total_sales

# account pdf generator
@login_required(login_url="/accounts/login")
def clientAccountPdfGenerator(request, pk):
    template_name = "reports/clientAccountPdf.html"
    client = get_object_or_404(Client, id=pk)
    client_transactions = models.Transaction.objects.filter(client=client)

    return render_to_pdf(
        template_name,
        {
            "client": client,
            "transactions": client_transactions,
            'date': datetime.now()
        },
    )

# sales pdf generation
# daily report
@login_required(login_url="/accounts/login")
def dailyReport(request):
    template_name = 'reports/salesPdf.html'
    # query today's expenses data
    sales = models.Transaction.objects.filter(date_created=date.today())
    return render_to_pdf(
        template_name,
        {
            "sales": sales,
            'title': 'Today(s) Sales',
            'date': date.today(),
            'total': salesTotal(sales)
        },
    )


# monthly report
@login_required(login_url="/accounts/login")
def monthlyReport(request):
    # computation for this month data
    today = date.today()
    current_month = today.month
    print(current_month)
    template_name = 'reports/salesPdf.html'
    sales = models.Transaction.objects.filter(date_created__month=current_month)
    print(sales)
    return render_to_pdf(
        template_name,
        {
            "sales": sales,
            'title': 'Monthly Sales',
            'date': date.today(),
            'total': salesTotal(sales)
        },
    )


