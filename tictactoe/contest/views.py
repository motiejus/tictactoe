from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import CodeUploadForm
from .models import Entry, LatestEntry, Fight, HandedOutCaps


def who_got_capped(request):
    caps = HandedOutCaps.objects.all()
    return render_to_response(
        'contest/who_got_capped.html', {'caps': caps},
        context_instance=RequestContext(request))


def entry(request, id):
    entry = get_object_or_404(Entry, pk=id)
    fights = Fight.objects.filter(Q(x=entry) | Q(o=entry)).order_by('id').all()
    return render_to_response(
        'contest/entry.html', {'entry': entry, 'fights': fights},
        context_instance=RequestContext(request))


def entries(request, uid=None):
    if uid is None:
        entries = Entry.objects
        user = None
    else:
        entries = Entry.objects.filter(user__id=uid)
        user = User.objects.get(id=uid)
    return render_to_response(
        'contest/entries.html', {'entries': entries.all(), 'user': user},
        context_instance=RequestContext(request))


def fight(request, id):
    fight = get_object_or_404(Fight, pk=id)
    return render_to_response(
        'contest/fight.html', {'fight': fight},
        context_instance=RequestContext(request))


def ranking(request):
    # Piggy-back 'results' to every value
    latest = LatestEntry.objects.all()
    res = [e.calc_results() for e in latest]
    [setattr(l, 'results', r) for l, r in zip(latest, res)]
    latest2 = sorted(latest, key=lambda x: x.results[0])

    return render_to_response(
        'contest/ranking.html', {'latestentries': latest2},
        context_instance=RequestContext(request))


@login_required
def upload(request):
    if request.method == 'POST':
        form = CodeUploadForm(request.POST)
        if form.is_valid():
            entry = form.instance
            entry.user = request.user
            entry.save()
            entry.qualify()
            messages.success(request, _("Code uploaded"))
            return redirect(entry.get_absolute_url())
    else:
        form = CodeUploadForm()
    return render_to_response(
        'contest/upload.html', {'form': form},
        context_instance=RequestContext(request))
