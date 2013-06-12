from django import template

import createQuizConstants as constants

register = template.Library()

@register.filter(is_safe=True)
def numtoupper(num):
    #Takes an integer and converts it to the equivalent uppercase letter. Values above 26 will get more letters, I.e. 27 outputs to AA.
    try:
        num = int(num)
    except: #Change nothing if an error is encountered
        return num
    
    letter = ""
    for i in range((num / 26) + 1):
        letter += constants.LETTERLIST[(num - 1) % 26]
    return letter

register.inclusion_tag('titleMenu.html')
def titlemenu(hasLogin):
    if not hasLogin:
        return {'login': "<a href='/create/login/'>Login</a> <a href='/create/register/'>Signup</a>"}
    else:
        return {'login': "<a>logout</a>"}
    