from decimal import Decimal
from django.db import connection

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer

from django.conf import settings
from sqlparse import format


def new_middleware(get_response):

    def middleware(request):
          response=get_response(request)

          if settings.DEBUG:
               num_queries= len(connection.queries)
               total_execution_time= Decimal()
               check_duplicate=set()
               for query in connection.queries:
                    total_execution_time += Decimal(query["time"])
                    check_duplicate.add(query["sql"])
                    formatsql=format(str(query["sql"]), reindent=True)
                    print(highlight(formatsql,SqlLexer(),TerminalFormatter()))

          print("==============")
          print("[statistiques des requestes sql]")
          print(f"{num_queries} Total de requetes")
          print(f"{num_queries - len(check_duplicate)} Total de double")
          print(f"{total_execution_time}")
          print("==============")
        #   q=list(connection.queries)
        #   for qs in q:
        #       formatsql=format(str(qs["sql"]), reindent=True)
        #       print(highlight(formatsql,SqlLexer(),TerminalFormatter()))
              
          return response
    return middleware