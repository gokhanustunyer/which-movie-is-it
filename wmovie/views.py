from django.shortcuts import render,HttpResponse,redirect

from code.searcher import Searcher


# Create your views here.
def index(request):
    return render(request,'index.html')

def search(request):

    if request.method == 'GET':return redirect('/')
    else : pass


def getResults(request):
    
    print(request.method)

    if request.method == 'GET':
        return redirect('/')

    elif request.method == 'POST':
        entrys = request.POST.get('getResult')
        s1 = Searcher()
        results = s1.start(entrys.split())
        
        return render(request,'movies.html',{'context':results})
