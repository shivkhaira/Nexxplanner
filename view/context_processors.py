from .models import Pro,Profile
from django.db.models import Q

def data(request):
    if request.user.is_authenticated and request.user.username != 'admin':
        user=Pro.objects.get(user=request.user)
        if request.session['profile']!=None:
            session = Profile.objects.get(Q(name=request.session['profile']) & Q(user=request.user.username))
            all=session.instagram+session.facebook+session.twitter
            instagram=session.instagram
            facebook=session.facebook
            twitter=session.twitter
            linkd=session.linkd
        else:
            instagram=0
            facebook=0
            twitter=0
            linkd=0
            all=0
        return {'session':request.session['profile'],'linkd':linkd,'instagram': instagram,'facebook':facebook,'twitter':twitter,'all':all,'profile':user.profile}
    else:
        return {'none':0}