from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'base.html')

def search(request):
    if request.method == "POST":
    	research_papers=[]
    	return render(request,"search.html",{"research_papers":research_papers})
    return render(request,"search.html")