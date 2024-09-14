from django.views.generic import ListView, DetailView

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

