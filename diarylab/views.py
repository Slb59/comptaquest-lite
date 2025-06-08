from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DiaryEntry
from .forms import DiaryEntryForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from django.utils.translation import gettext_lazy as _


class DiaryEntryCreateView(LoginRequiredMixin, CreateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = 'diarylab/add_entry.html'
    success_url = reverse_lazy('add_entry')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["title"] = _("Diary Lab")
        context["logo_url"] = "/static/images/logo_dl.png"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DiaryEntryListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = 'diarylab/list_entries.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["title"] = _("Diary Lab")
        context["logo_url"] = "/static/images/logo_dl_v02.png"
        context["form"] = DiaryEntryForm()
        entries = self.get_queryset()
        years = set(entry.date.year for entry in entries)
        months = set(entry.date.month for entry in entries)
        context['years'] = sorted(years)
        context['months'] = sorted(months)
        return context

def generate_pdf(request, year, month):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{year}{month:02d}-pensees.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    entries = DiaryEntry.objects.filter(user=request.user, date__year=year, date__month=month)

    for entry in entries:
        p.setFont("Helvetica", 12)
        p.drawString(100, 750, entry.date.strftime("%A %d %B %Y"))
        p.setFont("Helvetica", 10)
        text = p.beginText(100, 730)
        text.textLines(entry.content)
        p.drawText(text)
        p.showPage()

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
