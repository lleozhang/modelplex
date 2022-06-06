from User.models import User
import os

def check_login(request,ctx):
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') == 'true':
        if request.COOKIES.get('username'):
            name=request.COOKIES.get('username')
            var=User.objects.filter(name=name)
            if len(var)==1:
                var=var[0]
                if request.COOKIES.get('password'):
                    if var.password==request.COOKIES.get('password'):
                        ctx['username'] = request.COOKIES.get('username')
                        return (1,ctx)
    else:
        return (0,ctx)
    return (-1,ctx)