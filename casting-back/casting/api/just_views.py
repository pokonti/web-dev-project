from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponse, JsonResponse
from rest_framework.response import Response
from api.serializers import ApplicationsSerializer, CastingSerializer, FormSerializer, PositionSerializer, PositionSerializer2, AdSerializer
from rest_framework import status
from rest_framework.views import APIView
from .models import ApplicantToPosition, Casting, Form,Position,Ad
from rest_framework.decorators import api_view 
import json


from django.views.decorators.csrf import csrf_exempt

@api_view(["GET","POST"])
def get_castings(request):
    if request.method == 'GET':
        castings = Casting.objects.all()
        serializer = CastingSerializer(castings, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CastingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    


    # тут по id будет или по position name-> casting/dance/card1, casting/filming/card2????

# @api_view(["GET", "PUT","DELETE"])
# def casting_details(request, id):
#     try:
#         casting=Casting.objects.get(id=id)
#     except Casting.DoesNotExist as e :
#         return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
#     # ошибка 404
#     if request.method == "GET":
#         serializer = CastingSerializer(casting)
#         return Response(serializer.data)
    
#     elif request.method == "PUT":
#         serializer = CastingSerializer(
#             instance = casting,
#             data=request.data
#         )
#         if serializer.is_valid():
#             serializer.save()# update data...
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

#     elif request.method  == 'DELETE':
#         casting.delete()
#         return Response({"deleted": True})
    

def casting_positions(request, id):
    try:
        casting = Casting.objects.get(id=id)
    except Casting.DoesNotExist as e:
        return JsonResponse({"error": str(e)}, status=404)
    
    positions = Position.objects.filter(casting=casting)
    serializer = PositionSerializer2(positions, many=True)

    return JsonResponse(serializer.data, safe=False, status=200)
  



class PositionsDetailAPIView(APIView):
    def get(self, request, id = None, pk=None):
        try:
            casting_details(request=request, id=id)
            position =  Position.objects.get(pk=id)
        except Position.DoesNotExist as e:
            return Response({"error": str(e)}, status.HTTP_404_NOT_FOUND)
        
        serializer = PositionSerializer2(position)
        return Response(serializer.data)
    
    def put(self, request,id=None):
        try:
            position = Position.objects.get(id=id)
        except Position.DoesNotExist as e:
            return Response({"error": str(e)}, status.HTTP_404_NOT_FOUND)
        
        serializer = PositionSerializer2(instance=position, data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request,id=None):
        try:
            position = Position.objects.get(id=id)
        except Position.DoesNotExist as e:
            return Response({"error": str(e)}, status.HTTP_404_NOT_FOUND)
        
        position.delete()
        return Response({"deleted": True})


@api_view(["GET","POST"])
def get_ads(request):
    if request.method == 'GET':
        ad = Ad.objects.all()
        serializer = AdSerializer(ad, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    

# experiment 
@csrf_exempt 
def castings_list(request):
    if request.method == 'GET':
        castings = Casting.objects.all()
        serializer = CastingSerializer(castings, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        serializer = CastingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


def form_list(request):
    if request.method == 'GET':
        forms = Form.objects.all()
        serializer = FormSerializer(forms, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt 
def casting_details(request, id=None):
    try:
        casting = Casting.objects.get(id=id)
    except Casting.DoesNotExist as e:
        return JsonResponse({"error":str(e)}, status=400)
    
    if request.method == "GET":
        serializer = CastingSerializer(casting)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = json.loads(request.body)
        serializer = CastingSerializer(
            instance=casting,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        casting.delete()
        return JsonResponse({"deleted": True})
    

def appToPos(request):
    if request.method == 'GET':
        forms = ApplicantToPosition.objects.all()
        serializer = ApplicationsSerializer(forms, many=True)
        return JsonResponse(serializer.data, safe=False)
