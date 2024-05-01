# pdf_generation.py
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Payment
from .decorators import admin_accountant_required, login_required
from reportlab.lib.units import inch
from django.utils import timezone

@login_required
@admin_accountant_required
def generate_financial_statement(request):
    if request.method == 'POST':
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')

        if start_date and end_date:
            start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))  
            end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))  

            payments = Payment.objects.filter(date__range=[start_date, end_date])

            # Generate PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)

            # Add title
            p.setFont("Helvetica-Bold", 16)
            p.drawString(inch, 10.5 * inch, f"Financial Statement from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

            # Add payment details table
            data = [['User', 'Amount', 'Date']]
            total_amount = 0
            for payment in payments:
                data.append([payment.user.username, f"£{payment.amount}", payment.date.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d')])
                total_amount += payment.amount

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            # Adjust the y-coordinate where the table is drawn
            table.wrapOn(p, inch, 8.5 * inch)
            table.drawOn(p, inch, 8.5 * inch)

            # Add total amount
            p.setFont("Helvetica-Bold", 14)
            p.drawString(inch, 8 * inch, f"Total Amount: £{total_amount}")

            p.showPage()
            p.save()

            # File response
            buffer.seek(0)
            return HttpResponse(buffer, content_type='application/pdf')
        else:
            messages.error(request, 'Please select both start and end dates.')
    
    return redirect('users')

