from rest_framework import viewsets

from cryptocurrency.blockchains import models
from cryptocurrency.rest import serializers


class TransactionViewSet(viewsets.ModelViewSet):
    """The ViewSet for work with transactions.  """

    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()
