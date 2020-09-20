
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.

numlist = ['1','2','3','4','5','6','7','8','9','0']
oplist=['+','-','*','/','=']

def cal(request):
    try:
        context={}
        num_button = ''
        if request.method =='GET':
            dic={
                'display_html_value':0
            }
            return render(request,'calculator.html',dic)

        elif request.method =='POST':
            if not 'press' in request.POST:
                return render(request,'error.html')
            if 'press' in request.POST:

                button = request.POST['press']

                if button in numlist:
                    if request.POST['count_opn']=='':
                        context['count_op']=0
                    else:
                        context['count_op'] = 0
                        print('pp',context['count_op'],request.POST['count_opn'])
                  
                    num_button = int(button)

                    if not 'calc_display' in request.POST:
                        print("hihi")
                        return render(request,'error.html')
                    else:
                        if 'cur_valuen' in request.POST:
                            temp_cur = request.POST['cur_valuen']
                            print(temp_cur)
                            if temp_cur == '':
                                context['cur_value'] = num_button
                                context['display'] = num_button
                                context['display_html_value']=num_button

                            elif temp_cur in oplist:
                                if 'pre_operatorn' in request.POST:
                                    context['pre_operator'] = temp_cur
                                    context['pre_value'] = request.POST['pre_valuen']
                                    context['cur_value'] = num_button
                                    context['display']=num_button
                                    context['display_html_value'] = num_button

                            else:
                                temp_cur = int(temp_cur)
                                temp_cur = num_button + 10 * temp_cur
                                context['cur_value'] = temp_cur
                                context['pre_operator']=request.POST['pre_operatorn']
                                context['pre_value'] = request.POST['pre_valuen']
                                context['display'] =temp_cur
                                context['display_html_value'] = temp_cur
                                print('kkk')

                else:
                    operator = button
                    if 'cur_valuen' in request.POST:
                        temp_cur = request.POST['cur_valuen']
                        if temp_cur == '':
                            context['cur_value'] = 0

                        else:
                            if operator == 'plus':
                                context['cur_value'] = '+'

                            elif operator == 'minus':
                                context['cur_value'] = '-'

                            elif operator == 'times':
                                context['cur_value'] = '*'

                            elif operator == 'divide':
                                context['cur_value'] = '/'

                            elif operator == 'equals':
                                context['cur_value'] = '='
                    if not 'calc_display' in request.POST :
                        return render(request,'error.html')
                    
                    else:
                        if not 'count_opn' in request.POST:
                            return render(request,'error.html')
                        if int(request.POST['count_opn'])==0 :
                            context['count_op'] = 1

                            if 'pre_valuen' in request.POST:
                                context['display'] = request.POST['displayn']
                                context['display_html_value'] = request.POST['displayn']
                                context['pre_value'] = request.POST['displayn']

                            if request.POST['pre_operatorn']=='+':
                                context['display']=int(request.POST['pre_valuen']) + int(request.POST['cur_valuen'])
                                context['display_html_value'] = int(request.POST['pre_valuen']) + int(request.POST['cur_valuen'])
                                context['pre_value'] = int(request.POST['pre_valuen']) + int(request.POST['cur_valuen'])
                                context['pre_operator']=request.POST['pre_operatorn']

                            if request.POST['pre_operatorn']=='-':
                                context['display']=int(request.POST['pre_valuen']) - int(request.POST['cur_valuen'])
                                context['display_html_value'] = int(request.POST['pre_valuen']) - int(request.POST['cur_valuen'])
                                context['pre_value'] = int(request.POST['pre_valuen']) - int(request.POST['cur_valuen'])
                                context['pre_operator']=request.POST['pre_operatorn']
                            if request.POST['pre_operatorn']=='*':
                                context['display']=int(request.POST['pre_valuen']) * int(request.POST['cur_valuen'])
                                context['display_html_value'] = int(request.POST['pre_valuen']) * int(request.POST['cur_valuen'])
                                context['pre_value'] = int(request.POST['pre_valuen']) * int(request.POST['cur_valuen'])
                                context['pre_operator']=request.POST['pre_operatorn']
                            if request.POST['pre_operatorn']=='/':
                                context['display']=round(int(request.POST['pre_valuen']) / int(request.POST['cur_valuen']))
                                context['display_html_value'] = round(int(request.POST['pre_valuen']) / int(request.POST['cur_valuen']))
                                context['pre_value'] = round(int(request.POST['pre_valuen']) / int(request.POST['cur_valuen']))
                                context['pre_operator']=request.POST['pre_operatorn']

                        else:
                            context['count_op'] = int(request.POST['count_opn']) + 1
                            context['display']=request.POST['displayn']
                            context['display_html_value'] = request.POST['displayn']
                            context['pre_value']=request.POST['pre_valuen']
        return render(request, 'calculator.html', context)

    except (RuntimeError, ZeroDivisionError,TypeError,ValueError, NameError):
        print('i handled')
        return render(request,'error.html')


