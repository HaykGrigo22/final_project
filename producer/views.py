from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from home.models import Product
from producer.forms import ProducerForm, ProductFormSet
from producer.models import Producer


class ProducerList(ListView):
    model = Producer
    template_name = "producer/producers.html"
    context_object_name = 'producers'
    queryset = Producer.objects.all()


class ProducerDetailView(DetailView):
    model = Producer
    template_name = "producer/producer_detail.html"
    context_object_name = 'producer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producer = self.object

        context["products"] = Product.objects.filter(producer=producer)

        return context


class ProducerCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        producer_form = ProducerForm()
        product_formset = ProductFormSet(queryset=Product.objects.none())
        return render(request, 'producer/add_producer.html', {
            'producer_form': producer_form,
            'product_formset': product_formset,
        })

    def post(self, request, *args, **kwargs):
        producer_form = ProducerForm(request.POST, request.FILES)
        product_formset = ProductFormSet(request.POST, request.FILES)

        if producer_form.is_valid() and product_formset.is_valid():
            producer = producer_form.save()

            products = product_formset.save(commit=False)
            for product in products:
                product.producer = producer
                product.save()
            return redirect(producer.get_absolute_url())

        return render(request, 'producer/add_producer.html', {
            'producer_form': producer_form,
            'product_formset': product_formset,
        })


class UpdateProducerView(LoginRequiredMixin, UpdateView):
    model = Producer
    form_class = ProducerForm
    template_name = "producer/update_producer.html"

    def get_success_url(self):
        return reverse_lazy("producer:producer_detail",
                            kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        return super().get_object(queryset)


class DeleteProducerView(LoginRequiredMixin, DeleteView):
    model = Producer
    template_name = 'producer/delete_producer.html'
    success_url = reverse_lazy('producer:producers')

    def get_object(self, queryset=None):
        return super().get_object(queryset)
