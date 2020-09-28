from django.shortcuts import render
from calculator.forms import calculatorForm
# Create your views here.
def calculator(request):
    if request.method =="GET":
        return render(request,"calculator.html",{'form': calculatorForm()})
    form =calculatorForm(request.POST)
    if not form.is_valid():
        return render(request,"calculator.html",{'form':form})

    x=form.cleaned_data['x']
    y=form.cleaned_data['y']
    z= x/y
    return render(request,"calculator.html", {'form':calculatorForm(),'z':z,'x':x,'y':y})




def hello(request):
    return render(request,"hello.html")