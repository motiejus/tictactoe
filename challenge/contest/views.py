from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CodeUploadForm


@login_required
def upload(request):
    if request.method == 'POST':
        form = CodeUploadForm(request.POST)
        if form.is_valid():
            entry = form.instance
            entry.user = request.user
            entry.save()
            messages.success(request, _("Code uploaded"))
            return redirect(entry.get_absolute_url())
    else:
        form = CodeUploadForm()
    return render_to_response(
        'contest/upload.html', {'form': form},
        context_instance=RequestContext(request))
