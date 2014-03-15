from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CodeUploadForm
from .models import Entry, LatestEntry


def entry(request, id):
    entry = get_object_or_404(Entry, pk=id)
    return render_to_response(
        'contest/entry.html', {'entry': entry},
        context_instance=RequestContext(request))


def entries(request):
    entries = LatestEntry.objects.all()
    return render_to_response(
        'contest/entries.html', {'entries': entries},
        context_instance=RequestContext(request))


@login_required
def upload(request):
    if request.method == 'POST':
        form = CodeUploadForm(request.POST)
        if form.is_valid():
            entry = form.instance
            entry.user = request.user
            entry.save()
            entry.compete()
            messages.success(request, _("Code uploaded"))
            return redirect(entry.get_absolute_url())
    else:
        form = CodeUploadForm()
    return render_to_response(
        'contest/upload.html', {'form': form},
        context_instance=RequestContext(request))
