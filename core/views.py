from .models import SWOT, Contracts,Credits, Client, Valuta, Deposits, Reports
from django.core.urlresolvers import reverse,reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django import forms
from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML
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
        self.helper.form_class = 'card card-signup text-center'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-md-2 form-control'
        self.helper.field_class = 'col-md-4 col-md-offset-2 form-control'
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
