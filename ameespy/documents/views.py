from django.shortcuts import render
from .models import Document

def liste_documents(request):
    documents = Document.objects.all()
    return render(request, "documents/liste.html", {"documents": documents})
