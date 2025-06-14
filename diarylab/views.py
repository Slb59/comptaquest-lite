from io import BytesIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .forms import DiaryEntryForm
from .models import DiaryEntry

from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect


class DiaryEntryCreateView(LoginRequiredMixin, CreateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = "diarylab/add_entry.html"
    success_url = reverse_lazy("diarylab:list_entries")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["title"] = _("Diary Lab")
        context["logo_url"] = "/static/images/logo_dl_v02.png"

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Check if an entry already exists for the given date
        entry_date = form.cleaned_data['date']
        existing_entry = DiaryEntry.objects.filter(
            user=self.request.user,
            date=entry_date
        ).exists()

        if existing_entry:
            # Add an error to the form
            form.add_error('date', _("Une entrée existe déjà pour cette date."))
            # Re-render the form with the error message
            return self.form_invalid(form)
        
        # Save the form if no existing entry
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Re-render the form with errors
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
        # return render(self.request, self.template_name, {'form': form})


class DiaryEntryListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = "diarylab/list_entries.html"
    context_object_name = "entries"

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user).order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["title"] = _("Diary Lab")
        context["logo_url"] = "/static/images/logo_dl_v02.png"
        context["form"] = DiaryEntryForm()
        entries = self.get_queryset()
        years = set(entry.date.year for entry in entries)
        months = set(entry.date.month for entry in entries)
        context["years"] = sorted(years)
        context["months"] = sorted(months)

        # Check if there's an entry for today
        today = timezone.now().date()
        if entries.filter(date=today).exists():
            messages.error(self.request, _("Vous avez déjà saisi une pensée aujourd'hui."))
            context["entry_exists_today"] = entries.filter(date=today).exists()

        return context


def generate_pdf(request, year, month):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{year}{month:02d}-pensees.pdf"'

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
