from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cnnfgiapp.models import Fgi
from cnnfgiapp.serializers import FgiSerializer


@api_view(['GET', 'POST'])
def fgi_index(request):
    if request.method == 'GET':
        fgis = Fgi.objects.all()
        serializer = FgiSerializer(fgis, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FgiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)