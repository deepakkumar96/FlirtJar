from django.shortcuts import render


def api_doc_intro(request):
    return render(request, 'location/ApiIntro.html', {})
