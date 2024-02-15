from django.urls import path

from portfolio.views import index

urlpatterns = [
    path("<str:stock>/", index),
]
