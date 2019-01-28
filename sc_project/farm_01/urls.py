from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_api, name='dashboard_api'),
    path('dashboard/temp/<slug:device>', views.latest_temp, name='latest_temp'),
    path('dashboard/bpm/<slug:device>', views.latest_bpm, name='latest_bpm'),

#     path('<int:page>/<int:page_size>', views.dashboard_api, name='dashboard_api')
#    path('api/farm_01/dev/', views.Bt_dev_ListCreate.as_view() ),
#    path('api/farm_01/data/', views.Bt_data_ListCreate.as_view() ),
]
