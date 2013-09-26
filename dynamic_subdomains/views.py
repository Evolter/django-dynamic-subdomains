import urllib

from django.http import HttpResponseRedirect, HttpResponseBadRequest

from .forms import RedirectForm


def redirect(request):
    form = RedirectForm(request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest(repr(form.errors))

    parameters = request.GET.copy()
    for key in ['domain', 'path']:
        if key in parameters:
            del parameters[key]
    parameters = urllib.urlencode(parameters)

    url = form.cleaned_data['path']
    if parameters:
        url = '%s?%s' % (url, parameters)

    response = HttpResponseRedirect(url)
    response.set_cookie('_domain', form.cleaned_data['domain'])
    response.status_code = 307  # Re-submit POST requests

    return response
