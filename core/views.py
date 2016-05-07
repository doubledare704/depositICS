from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from depositICS.settings import CURRENCY
from .models import SWOT, Contracts, Credits, Reports


# Create your views here.

class LoginRequiredMixin(object):
    """
    A login required mixin for use with class based views. This Class is a light wrapper around the
    `login_required` decorator and hence function parameters are just attributes defined on the class.

    Due to parent class order traversal this mixin must be added as the left most
    mixin of a view.

    The mixin has exaclty the same flow as `login_required` decorator

    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class SwotListView(LoginRequiredMixin, ListView):
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


class SwotCreateView(LoginRequiredMixin, SwotViewMixin, CreateView):
    form_class = SwotForm
    success_msg = 'Атрибут додано'
    cancel_id = 'cancel_button'
    cancel_msg = 'Зупинка'


class SwotUpdateView(LoginRequiredMixin, SwotViewMixin, UpdateView):
    form_class = SwotUpdateForm
    success_msg = 'Оновлено атрибут'
    cancel_id = 'cancel_button'
    cancel_msg = 'Редагування зупинено'


class SwotDeleteView(LoginRequiredMixin, DeleteView):
    model = SWOT
    template_name = "core/delete_confirm.html"

    def get_success_url(self):
        return '{0}'.format(reverse_lazy('swot'))


class AnalysisListView(LoginRequiredMixin, TemplateView):
    template_name = "core/analysis.html"

    def get_context_data(self, **kwargs):
        context = super(AnalysisListView, self).get_context_data(**kwargs)

        time_threshold = datetime.now() - relativedelta(years=1)

        creds_dates = Credits.objects.all().filter(
            date_credit__gte=time_threshold).values('date_credit', ).annotate(sum=Sum('all_sum')).order_by(
            'date_credit')

        time_threshold = datetime.now() - relativedelta(years=1)
        summary = Contracts.objects.all().filter(datestart__gte=time_threshold).values(
            'datestart', 'id_deposits__id_valuta__name', 'id_deposits__duration', 'id_client__type_cl').annotate(
            sum=Sum('suma')).order_by(
            '-id_deposits__id_valuta__name')
        # get sums for same months
        per_month = defaultdict(Decimal)
        per_duration = {'12': 0, '6': 0, '3': 0}
        per_client = {'фізична особа': 0, 'банк': 0, 'юридична особа': 0}
        # get sum with same months in credits
        for s in summary:
            s['sum'] *= CURRENCY.get(s['id_deposits__id_valuta__name'], 1)
            month = s['datestart'].year, s['datestart'].month
            per_month[month] += s['sum']
            duration = str(s['id_deposits__duration'])
            per_duration[duration] += s['sum']
            client = s['id_client__type_cl']
            per_client[client] += s['sum']
        # needed keys for client type
        needed_client = ('фізична особа', 'юридична особа')
        sumka = 0
        # sum if needed type in per_client
        for i in range(len(needed_client)):

            sumka += per_client[needed_client[i]]
            if sumka > per_client['банк']:
                type_decision = 'Не потрібно управлінських рішень'
                type_expl = 'Суми за юр. і фіз. особами > суми з інших банків'
            else:
                type_decision = 'Переглянути депозитні програми і залучити нових клієнтів (юр і фіз осіб)'
                type_expl = 'Суми за юр. і фіз. особами < суми з інших банків'
        # write to context all data
        context['types'] = per_client
        context['t_dec'] = type_decision
        context['t_expl'] = type_expl
        context['t_suma'] = sumka

        # check for maximum value for some unknown key, when finds max value returns key
        max_key = max(per_duration, key=lambda k: per_duration[k])

        if int(max_key) > 6:
            duration_decision = 'Переглянути наявні депозитні програми, зменшити відсоткові ставки довгостр. депозитів'
            duration_expl = 'Довгострокові > Короткострокові'
        else:
            duration_decision = 'Не потрібно управлінських рішень'
            duration_expl = 'Довгострокові < Короткострокові'

        # write to context
        context['duration'] = per_duration
        context['dur_dec'] = duration_decision
        context['dur_expl'] = duration_expl

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
                        explain = 'Сума депозитів більша за суму кредитів'
                    elif 1.05 > coef > 0.95:
                        decision = 'Ніякі рішення не потрібні'
                        explain = 'Сума депозитів майже рівноважна з  сумою кредитів'
                    elif coef < 0.95:
                        decision = 'Створити акційні пропозиції, переглядати або створити депозитні' \
                                   ' програми'
                        explain = 'Сума депозитів менша за суму кредитів'
                    difference.append({
                        'depos': val,
                        'creds': sumc,
                        'date': dat,
                        'df': val - sumc,
                        'dc': decision,
                        'explain': explain,
                        'pr': val - sum(per_month.values()) / len(per_month)
                    })
        context['difs'] = difference

        return context


class ReportListView(LoginRequiredMixin, ListView):
    model = Reports
    template_name = "core/reports.html"


class ReportForm(SwotForm):
    class Meta:
        model = Reports
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

        self.helper.form_action = reverse('report_add')
        self.helper.layout[-1] = FormActions(
            Submit('add_button', 'Зберегти',
                   css_class='btn btn-primary'),
            HTML(
                '<a class="btn btn-warning" href="{0}">{1}</a>'.format(reverse('report'), 'Відміна')),
        )


class ReportUpdateForm(ReportForm):
    def __init__(self, *args, **kwargs):
        super(ReportUpdateForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('report_edit', kwargs={'pk': kwargs['instance'].id})


class ReportMixin(SwotViewMixin):
    model = Reports

    def get_success_url(self):
        return '{0}'.format(reverse_lazy('report'))


class ReportCreateView(LoginRequiredMixin, ReportMixin, CreateView):
    form_class = ReportForm
    success_msg = 'Звіт додано'
    cancel_id = 'cancel_button'
    cancel_msg = 'Зупинка'


class ReportUpdateView(LoginRequiredMixin, ReportMixin, UpdateView):
    form_class = ReportUpdateForm
    success_msg = 'Оновлено звіт'
    cancel_id = 'cancel_button'
    cancel_msg = 'Редагування зупинено'


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Reports
    template_name = "core/delete_report.html"

    def get_success_url(self):
        return '{0}'.format(reverse_lazy('report'))
