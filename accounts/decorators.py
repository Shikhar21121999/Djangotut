from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    '''
    A decorator for view function
    It add functionality that view function only vissible
    if user is not authenticated.
    Used to restrict acess to register and login page for authenticated user
    '''
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper


def allowed_user_group(allowed_roles=[]):
    '''
    A decorator to add functionality that only the list of 
    roles or groups passed can acces the following function
    '''

    def decorator(view_func):
        '''
        Actual decorator that restricts the passed in func
        for some users
        '''
        def wrapper(request, *args, **kwargs):
            '''
            wrapper function for constructor
            '''

            group = None

            # get the first group to which current user is part of
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            # check if this user has acess to the view function
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Not allowed to view this content')
        return wrapper
    return decorator
