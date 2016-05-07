from .models import SWOT, Contracts, Credits, Client, Valuta, Deposits, Reports
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from django import forms
from django.contrib import messages
from django.db.models import Sum

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML

from datetime import datetime
from dateutil.relativedelta import relativedelta
from depositICS.settings import CURRENCY
from collections import defaultdict
from decimal import Decimal


# Create your views here.


class SwotListView(ListView):
    model = SWOT
    template_name = "core/swot.html"


class SwotForm(forms.ModelForm):
    class Meta:
        model = SWOT
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SwotForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('swot_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal text-center'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'input-group col-md-6'
        self.helper.layout.append('')
        self.helper.layout[-1] = FormActions(
            Submit('add_button', 'Зберегти',
                   css_class='btn btn-primary'),
            HTML(
                '<a class="btn btn-warning" href="{0}">{1}</a>'.format(reverse('swot'), 'Відміна')),
        )


class SwotUpdateForm(SwotForm):
    def __init__(self, *args, **kwargs):
        super(SwotUpdateForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('swot_edit', kwargs={'pk': kwargs['instance'].id})


class SwotViewMixin(object):
    model = SWOT
    template_name = "core/swot_edit.html"

    def get_success_url(self):
        return '{0}'.format(reverse_lazy('swot'))

    def post(self, request, *arg, **kwargs):
        if request.POST.get(self.cancel_id):
            messages.info(self.request, self.cancel_msg)
        else:
            messages.success(self.request, self.success_msg)
            return super(SwotViewMixin, self).post(
                request, *arg, **kwargs)


class SwotCreateView(SwotViewMixin, CreateView):
    form_class = SwotForm
    success_msg = 'Атрибут додано'
    cancel_id = 'cancel_button'
    cancel_msg = 'Зупинка'


class SwotUpdateView(SwotViewMixin, UpdateView):
    form_class = SwotUpdateForm
    success_msg = 'Оновлено атрибут'
    cancel_id = 'cancel_button'
    cancel_msg = 'Редагування зупинено'


class SwotDeleteView(DeleteView):
    model = SWOT
    template_name = "core/delete_confirm.html"

    def get_success_url(self):
        return '{0}'.format(reverse_lazy('swot'))


class AnalysisListView(TemplateView):
    template_name = "core/analysis.html"

    def get_context_data(self, **kwargs):
        context = super(AnalysisListView, self).get_context_data(**kwargs)

        time_threshold = datetime.now() - relativedelta(years=1)

        creds_dates = Credits.objects.all().filter(
            date_credit__gte=time_threshold).values('date_credit',).annotate(sum=Sum('all_sum')).order_by('date_credit')

        time_threshold = datetime.now() - relativedelta(years=1)
        summary = Contracts.objects.all().filter(datestart__gte=time_threshold).values(
            'datestart', 'id_deposits__id_valuta__name').annotate(sum=Sum('suma')).order_by(
            '-id_deposits__id_valuta__name')
        # get sums for same months
        per_month = defaultdict(Decimal)
        for s in summary:
            s['sum'] *= CURRENCY.get(s['id_deposits__id_valuta__name'], 1)
            month = s['datestart'].year, s['datestart'].month
            per_month[month] += s['sum']
        # get sum with same months in credits
        finals = {}
        for c in creds_dates:
            monthc = c['date_credit'].year, c['date_credit'].month
            finals[monthc] = c['sum']
        # find the diffs between deposits and credits
        difference = []
        for key, val in per_month.items():
            for dat, sumc in finals.items():
                if key == dat:
                    coef = val / sumc
                    if coef > 1.05:
                        decision = 'Слід знижувати відсоткові ставки в депозитних програмах'
                    elif 1.05 > coef > 0.95:
                        decision = 'Ніякі рішення не потрібні'
                    elif coef < 0.95:
                        decision = 'Створити акційні пропозиції, переглядати або створити депозитні' \
                                                 ' програми'
                    difference.append({
                        'depos': val,
                        'creds': sumc,
                        'date': dat,
                        'df': val-sumc,
                        'dc': decision,
                        'pr': val - sum(per_month.values())/len(per_month)
                    })
        print(difference)
        context['difs'] = difference
        return context
