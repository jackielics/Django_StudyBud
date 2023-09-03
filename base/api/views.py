from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
# from base.api import serializers


@api_view(['GET']) # Allow Methods
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    '''Get All Rooms'''
    rooms = Room.objects.all()
    # Python Obj to Json Obj 
    serializer = RoomSerializer(rooms, many=True) # all()
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    '''Get a Specific Room'''
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
