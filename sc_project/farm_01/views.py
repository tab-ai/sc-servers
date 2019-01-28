# from django.shortcuts import render

from .models import Bt_dev, Bt_data
from .serializers import Bt_dev_Serializer, Bt_data_Serializer
from rest_framework import generics, viewsets

# django_rest_api_custom
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# template
from django.views.generic import TemplateView

catchall = TemplateView.as_view(template_name='index.html')



# Dashboard Api
@api_view(['GET'])
def dashboard_api(request):
    # connect check (sort bt_id)
    connect_device_list = sorted(Bt_dev.objects.filter(status="connect"), key=lambda x : (x.bt_id, len(x.bt_id)))

    # dashboard api get
    if request.method == 'GET':
        dashboard_api_list = list()

        for dev_obj in connect_device_list:
            dashboard_api_dict = dict()
            try:
                bt_data_get = Bt_data.objects.filter(bt_id=dev_obj.bt_id).latest('time')
                dashboard_api_dict["bt_id"] = bt_data_get.bt_id
                dashboard_api_dict["address"] = dev_obj.bt_address
                dashboard_api_dict["battery"] = round(bt_data_get.battery)
                dashboard_api_dict["time"] = int(dev_obj.time.timestamp()*1000.)
                dashboard_api_dict["pk"] = dev_obj.pk

                # dashboard_api_list append
                dashboard_api_list.append(dashboard_api_dict)
            except:
                pass

        return Response(dashboard_api_list)


# latest_temp
@api_view(['GET'])
def latest_temp(request, device):
    # connect check (sort bt_id)
    try:
       connect_device = Bt_dev.objects.get(status="connect", bt_id=device)
    except:
       return Response(status=status.HTTP_404_NOT_FOUND)

    # dashboard api get
    if request.method == 'GET':
        dashboard_api_dict = dict()
        try:
            bt_data_get = Bt_data.objects.filter(bt_id=connect_device.bt_id).latest('time')
            dashboard_api_dict["bt_id"] = bt_data_get.bt_id
            dashboard_api_dict["temp"] = bt_data_get.temp
            dashboard_api_dict["time"] = int(connect_device.time.timestamp()*1000.)
        except:
            pass

        return Response(dashboard_api_dict)


# latest_bpe
@api_view(['GET'])
def latest_bpm(request, device):
    # connect check (sort bt_id)
    try:
       connect_device = Bt_dev.objects.get(status="connect", bt_id=device)
    except:
       return Response(status=status.HTTP_404_NOT_FOUND)

    # dashboard api get
    if request.method == 'GET':
        dashboard_api_dict = dict()
        try:
            bt_data_get = Bt_data.objects.filter(bt_id=connect_device.bt_id).latest('time')
            dashboard_api_dict["bt_id"] = bt_data_get.bt_id
            dashboard_api_dict["bpm"] = bt_data_get.bpm
            dashboard_api_dict["time"] = int(connect_device.time.timestamp()*1000.)
        except:
            pass

        return Response(dashboard_api_dict)



# Bt_dev
class Bt_dev_ViewSet(viewsets.ModelViewSet):
    queryset = Bt_dev.objects.all()
    serializer_class = Bt_dev_Serializer

class Bt_dev_ListCreate(generics.ListCreateAPIView):
    queryset = Bt_dev.objects.all()
    serializer_class = Bt_dev_Serializer


# Bt_data
class Bt_data_ViewSet(viewsets.ModelViewSet):
    queryset = Bt_data.objects.all()
    serializer_class = Bt_data_Serializer


class Bt_data_ListCreate(generics.ListCreateAPIView):
    queryset = Bt_data.objects.all()
    serializer_class = Bt_data_Serializer
