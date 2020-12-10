from .models import Pro,Profile
from django.db.models import Q

def data(request):
    if request.user.is_authenticated and request.user.username != 'admin':
        user=Pro.objects.get(user=request.user)
        sessionx = Profile.objects.filter(user=request.user.username)
        if request.session['profile']!=None:
            session = Profile.objects.get(Q(name=request.session['profile']) & Q(user=request.user.username))
            all=session.instagram+session.facebook+session.twitter+session.linkd
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
        return {'linkd':linkd,'instagram': instagram,'facebook':facebook,'twitter':twitter,'all':all,'session':request.session['profile'],'tprofile':user.profile,'limit':user.limit,'profile':sessionx}
    else:
        return {'none':0}