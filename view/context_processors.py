from .models import Pro

def data(request):
    if request.user.is_authenticated and request.user.username != 'admin':
        user=Pro.objects.get(user=request.user)
        all=user.instagram+user.facebook+user.twitter
        return {'instagram': user.instagram,'facebook':user.facebook,'twitter':user.twitter,'all':all}
    else:
        return {'none':0}