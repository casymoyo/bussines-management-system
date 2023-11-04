import datetime
from datetime import timezone
from django.db.models import Q, Sum
from django.contrib import messages
from expenses.forms import ExpensesForm
from expenses.models import Expense, ExpenseCancellation
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_list_or_404

# pdf
from config.utils import render_to_pdf


@login_required(login_url="/accounts/login")
def Expenses(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    expenses = Expense.objects.filter(
        Q(date_created__icontains=q) |
        Q(name__icontains=q) |
        Q(amount__icontains=q) |
        Q(user__name__icontains=q)
    )
    # processing expense creation
    form = ExpensesForm()
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            exp_obj = form.save(commit=False)
            exp_obj.user = request.user
            exp_obj.save()
            messages.success(request, 'Expense successfully created')
            return redirect('expenses:expenses')
        messages.warning(request, 'Failed to create expense')
    return render(request, 'expenses/expenses.html', {
        'expenses': expenses or Expense.objects.all(),
        'form': form
    })


@login_required(login_url="/accounts/login")
def ExpenseCancellation(request, pk):
    exp = get_list_or_404(Expense, id=pk)
    if request.method == 'POST':
        exp_obj = ExpenseCancellation(
            user=request.user,
            expense=exp,
            reason=request.POST['reason']
        )
        exp_obj.save()
        messages.success(request, 'Expense successfully cancelled')
        return redirect('expenses:expenses')
    messages.warning(request, 'cancellation failed')
    return redirect('expenses:expenses')


# function for total amount of expenses computation
# worried with performance as the dataset increases :(
def expensesTotal(expenses_data):
    total_expenses = 0
    exp = expenses_data.annotate(total=Sum('amount'))
    for exp in exp:
        total_expenses = exp.amount + total_expenses
    return total_expenses


# daily report
@login_required(login_url="/accounts/login")
def dailyReport(request):
    template_name = 'reports/expensesPdf.html'
    # query today's expenses data
    expenses = Expense.objects.filter(date_created=datetime.date.today())
    return render_to_pdf(
        template_name,
        {
            "expenses": expenses,
            'title': 'Today(s) Expenses',
            'date': datetime.date.today(),
            'total': expensesTotal(expenses)
        },
    )


# monthly report
@login_required(login_url="/accounts/login")
def monthlyReport(request):
    # computation for this month data
    today = datetime.date.today()
    current_month = today.month

    template_name = 'reports/expensesPdf.html'
    expenses = Expense.objects.filter(date_created__month=current_month)
    return render_to_pdf(
        template_name,
        {
            "expenses": expenses,
            'title': 'Monthly Expenses',
            'date': datetime.date.today(),
            'total': expensesTotal(expenses)
        },
    )


@login_required(login_url="/accounts/login")
def customReport(request):
    end_date = request.GET['date_from']
    start_date = request.GET['date_to']
    print(end_date, start_date)
    template_name = 'reports/expensesPdf.html'

    expenses = Expense.objects.filter(date_created__gte=start_date, date_created__lte=end_date)
    print(expenses)
    return render_to_pdf(
        template_name,
        {
            "expenses": expenses,
            'title': 'Today(s) Expenses',
            'date': datetime.date.today(),
            # 'total': custom_total_amount['amount__sum']
        },
    )
