from django.shortcuts import render

from .models import Produit
import json
from django.http import JsonResponse
from django.core.serializers import serialize

from django.db import connection

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer

from sqlparse import format


# Create your views here.


def index(request):
    qs=Produit.objects.all()
    serializerqs= serialize("json", qs)
    # q=list(connection.queries)
    # for qs in q:
    #     formatsql=format(str(qs["sql"]), reindent=True)
    #     print(highlight(formatsql,SqlLexer(),TerminalFormatter()))


    serializer_data=json.loads(serializerqs)
    return JsonResponse(serializer_data, safe=False,status=200)
