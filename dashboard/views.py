from django.shortcuts import render
from django.views import View

class Index(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'dashboard/index.html')
