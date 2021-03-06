from django.db.models import Q
from django.shortcuts import render, reverse
from django.conf import settings

from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView, View

from extra_views import InlineFormSet, CreateWithInlinesView
from extra_views.generic import GenericInlineFormSet

from models import Customer, Product, Quotation, QuotationLine, STATUS_CHOICES, Bill, BillLine

import json

from form import QuotationLineForm


from django.core.mail import EmailMessage
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.http import HttpResponse

class IndexView(TemplateView):
    template_name = "main_app/index.html"


# /////////////////////////////////
class ListCustomerView(ListView):
    model = Customer

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        print "QUERY=", query

        if query != None:

            return Customer.objects.filter(
                Q(first_name__contains=query) | Q(last_name__contains=query)
                | Q(zipcode__contains=query) | Q(business__contains=query))

        else:
            return Customer.objects.all()


class CreateCustomerView(CreateView):
    model = Customer
    fields = "__all__"

    def get_success_url(self):
        return reverse("detail-customer", args=[self.object.slug])


class DetailCustomerView(DetailView):
    model = Customer


class UpdateCustomerView(UpdateView):
    model = Customer
    fields = "__all__"

    def get_success_url(self):
        return reverse("detail-customer", args=[self.object.slug])


class DeleteCustomerView(DeleteView):
    model = Customer

    def get_success_url(self):
        return reverse("customers")


# /////////////////////////////////


class ListProductView(ListView):
    model = Product

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        print "QUERY=", query

        if query != None:

            return Product.objects.filter(
                Q(name__contains=query) | Q(code__contains=query))

        else:

            return Product.objects.all()


class CreateProductView(CreateView):
    model = Product
    fields = "__all__"

    def get_success_url(self):
        return reverse("detail-product", args=[self.object.code])


class DetailProductView(DetailView):
    model = Product
    slug_field = 'code'
    slug_url_kwarg = 'code'


class UpdateProductView(UpdateView):
    model = Product
    fields = (
        'name',
        'description',
        'short_desc',
        'pics',
        'price',
    )
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_success_url(self):
        return reverse("detail-product", args=[self.object.code])


class DeleteProductView(DeleteView):
    model = Product
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_success_url(self):
        return reverse("products")


# /////////////////////////////////


class QuotationLineInLine(InlineFormSet):
    model = QuotationLine
    fields = "__all__"


class QuotationFormSetView(CreateWithInlinesView):
    template_name = 'main_app/quotation_form.html'
    model = Quotation
    success_url = '/quotation'
    inlines = [
        QuotationLineInLine,
    ]
    fields = "__all__"


class ListQuotationView(ListView):
    model = Quotation

    def get_queryset(self, *args, **kargs):
        query = self.request.GET.get('q', None)
        filter = self.request.GET.get('status', None)

        print "QUERY=", query

        if query != None and filter != None:

            return Quotation.objects.filter(
                Q(status__contains=filter) &
                (Q(customer__first_name__contains=query)
                 | Q(customer__last_name__contains=query)
                 | Q(customer__zipcode__contains=query)
                 | Q(customer__business__contains=query)))

        else:

            return Quotation.objects.all()


class DetailQuotationView(DetailView):
    model = Quotation
    slug_field = 'customer'
    slug_url_kwarg = 'customer'

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self)
        context['status_choices'] = STATUS_CHOICES
        context['form'] = QuotationLineForm(initial={"quotation": self.object})
        return context


class DeleteQuotationView(DeleteView):
    model = Quotation
    template_name = 'main_app/quotation_detail.html'
    def get_success_url(self):

        return reverse("quotation")


def send_pdf(request, pk):

    quotation = Quotation.objects.get(id=pk)
    print quotation, type(quotation)
    context = {'quotation': quotation}
    context['total'] = 0

    lines = QuotationLine.objects.filter(quotation=pk)

    for line in lines:
        context['total'] += line.quantity * line.product.price

    context['ttc'] = context['total']*20.6
    # print context, type(context)

    html = render_to_string('main_app/quotation_detail_pdf.html', context)
    # print html

    filename = 'quotation_' + pk + '_'+ quotation.customer.first_name + '_' + quotation.customer.last_name + '.pdf'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=' + filename
    # print response

    pdf = HTML(string=html).write_pdf(
        stylesheets=[CSS(string='body { font-family: serif}')]
    )

    to_emails = [quotation.customer.email]

    subject = "French-E Quotation du :" + quotation.date.strftime('%Y-%m-%d %H:%M')


    email = EmailMessage(
        subject, body=pdf, from_email=settings.EMAIL_HOST_USER, to=to_emails
    )

    email.attach(response['Content-Disposition'], pdf, "application/pdf")

    email.content_subtype = "pdf"  # Main content is now text/html
    email.encoding = 'us-ascii'
    email.send()

    return HttpResponse(pdf, content_type='application/pdf')

#///////////////////////////////////////////////////////////////////////////////////

class BillView(View):
    # success_url = "/bills"

    def post(self, request, *args, **kwargs):
        id_quotation = request.POST.get('quotation')
        quotation = Quotation.objects.filter(id=id_quotation)[0]
        bill = Bill.objects.create(quotation=quotation)
        lines = QuotationLine.objects.filter(quotation = quotation)
        for line in lines:
            BillLine.objects.create(bill=bill, product=line.product, quantity=line.quantity)



class ListBillView(ListView):
    model = Bill

    def get_queryset(self, *args, **kargs):
        query = self.request.GET.get('q', None)
        filter = self.request.GET.get('status', None)

        print "QUERY=", query

        if query != None and filter != None:

            return Bill.objects.filter(
                Q(status__contains=filter) &
                (Q(customer__first_name__contains=query)
                 | Q(customer__last_name__contains=query)
                 | Q(customer__zipcode__contains=query)
                 | Q(customer__business__contains=query)))

        else:

            return Bill.objects.all()


class DetailBillView(DetailView):
    model = Bill
    slug_field = 'customer'
    slug_url_kwarg = 'customer'
