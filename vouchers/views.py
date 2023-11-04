import os
from vouchers.models import *
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from vouchers.forms import addVoucherFileForm

@login_required(login_url="/accounts/login")
def voucherFiles(request):
    files = voucherFile.objects.all()
    form = addVoucherFileForm()
    if request.method == 'POST':
        form = addVoucherFileForm(request.POST, request.FILES)
        if form.is_valid():
            voucher_object = form.save(commit = False)
            voucher_object.user = request.user
            voucher_object.save()
    return render(request, 'vouchers/vouchers.html', {
        'voucherFiles': files.filter(status = 'not populated'),
        'form': form
    })

@login_required(login_url="/accounts/login")
def vouchersList(request):
    vou = vouchers.objects.all()
    categories = voucherCategory.objects.all()
    q =  request.GET.get('q') if request.GET.get('q') != None else ''
    try:
        filtered_vouchers = vou.filter(file__category = q) & vou.filter(status = 'unused')
    except:
        filtered_vouchers = vou.all() & vou.filter(status = 'unused')

    return render(request, 'vouchers/vouchers_list.html', {
        'vouchers': filtered_vouchers,
        'categories':categories
    })

@login_required(login_url="/accounts/login")
def addCategory(request):
    if request.method  == 'POST':
        print(request.POST['name'])
        category_name = request.POST['name']
        if voucherCategory.objects.filter(name = category_name).exists():
            messages.warning(request, 'category exists')
            return redirect('vouchers:voucherFiles')
        new_category = voucherCategory(
            name = category_name
        )
        new_category.save()
    messages.success(request, 'category successfully added')
    return redirect('vouchers:voucherFiles')

@login_required(login_url="/accounts/login")  
def populateVouchers(request, pk):
    files = voucherFile.objects.all()
    try:
        file = voucherFile.objects.get(pk=pk)
    except:
        return render(request, '404.html')

    if file.status == 'not populated':
        file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
        print(file_path)
        with open(file_path, "r") as f:
            for voucher_number in f:
                voucher = vouchers(
                    user_id = request.user.id,
                    voucher_no = voucher_number.strip(),
                    file = file
                )
                voucher.save()
            file.status = 'populated'
            file.save()
            messages.success(request, "Vouchers Successfully Populated." )
            return redirect('vouchers:voucherList')
    else:
        messages.error(request, "File is already populated")
    return render(request, 'vouchers/vouchers.html', {'voucherFiles': files}) 

# @login_required(login_url='/users/login/')
# def voucherLog(request):
#     logs = voucherLogs.objects.all()
#     q = request.GET.get('q') if request.GET.get('q') != None else ''

#     if q == 'create':
#         return render(request, 'vouchers/voucherLogs.html', {
#             'logs': logs.filter(Q(action__icontains = q ))
#         })
#     elif q == 'print':
#         return render(request, 'vouchers/voucherLogs.html', {
#             'logs': logs.filter(Q(action__icontains = q ))
#         })
#     elif q == 'populate':
#         return render(request, 'vouchers/voucherLogs.html', {
#             'logs': logs.filter(Q(action__icontains = q ))
#         })
    
#     return render(request, 'vouchers/voucherLogs.html',
#         {'logs': logs or voucherLogs.objects.filter(
#             Q(user__username__icontains = q) |
#             Q(action__icontains = q)|
#             Q(date_created__icontains = q)
#         )}
#     )
