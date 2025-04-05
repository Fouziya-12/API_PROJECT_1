from django.shortcuts import render
from .models import Carlist,Showroomlist,Review
from django.http import JsonResponse
from .api_file.serializers import CarSerializer,ShowroomSerializer,ReviewSerializers
from .api_file.permissions import AdminOrReadOnlyPermission,ReviewUserorReadonlypermission
from rest_framework.response import Response
from rest_framework.decorators import api_view
from  django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework import mixins
# from django.core.exceptions import ValidationError
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from rest_framework.exceptions import ValidationError
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from .api_file.throttling import ReviewDetailThrottle,Reviewlistthrottle
from .api_file.pagination import Reviewlistpagination,Reviewlistlimitoffpag,Reviewlistcursorpag

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializers
# to avoid multiple times reviews by same user
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self,serializer):
        pk = self.kwargs['pk']
        cars = Carlist.objects.get(pk=pk)  
        useredit = self.request.user
        Review_queryset = Review.objects.filter(car=cars,apiuser=useredit)  
        if Review_queryset.exists():
            raise ValidationError("You have already reviwed this car")
        serializer.save(car=cars,apiuser=useredit )

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [ReviewUserorReadonlypermission]
    # authentication_classes = [TokenAuthentication]
    # throttle_classes = [Reviewlistthrottle,AnonRateThrottle]
    # throttle_classes = [ScopedRateThrottle] 
    # throttle_scope = 'review_list_scope'
    # pagination_class = Reviewlistpagination
    # pagination_class = Reviewlistlimitoffpag
    pagination_class = Reviewlistcursorpag
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(car=pk)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):   # (RetrieveAPIView,UpdateAPIView,DestoryAPIView)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    authentication_classes = [TokenAuthentication]
    # throttle_classes = [ReviewDetailThrottle,AnonRateThrottle] 
    # permission_classes = [AdminOrReadOnlyPermission]
    throttle_classes = [ScopedRateThrottle] 
    throttle_scope = 'review_list_scope'
    permission_classes = [ReviewUserorReadonlypermission]
   

# class ReviewDetails(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializers
#     def get(self,request, *args, **kwargs):
#         return self.retrieve(request,*args,**kwargs)


# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializers
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [DjangoModelPermissions]

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
 
class Showroom_Viewset(viewsets.ReadOnlyModelViewSet):
    queryset = Showroomlist.objects.all()
    serializer_class = ShowroomSerializer



# class Showroom_Viewset(viewsets.ViewSet):
#     def list(self,request):
#         qureyset = Showroomlist.objects.all()
#         serializer = ShowroomSerializer(qureyset,many=True, context={'request': request})
#         return Response(serializer.data)

#     def retrieve(self,request,pk=None):
#         queryset = Showroomlist.objects.all()
#         user = get_object_or_404(queryset,pk=pk)
#         serializer = ShowroomSerializer(user,context={'request': request})
#         return Response(serializer.data)

#     def create(self,request):
#         serializer = ShowroomSerializer(data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class Showroom_View(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAdminUser]



    def get(self,request):
        showroom = Showroomlist.objects.all()
        serializer = ShowroomSerializer(showroom ,many=True,context={'request': request})
        return Response(serializer.data)

    def post(self,request):
        serializer = ShowroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Showroom_Details(APIView):
    def get(self,request,pk):
        try:
            showroom = Showroomlist.objects.get(pk=pk)
        except Showroomlist.DoesNotExist:
            return Response({'Error':'Showroom Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ShowroomSerializer(showroom, context={'request': request})
        return Response(serializer.data)


    def put(self,request,pk):
        showroom = Showroomlist.objects.get(pk=pk)
        serializer = ShowroomSerializer(showroom,data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        showroom = Showroomlist.objects.get(pk=pk)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        

# import json
# Create your views here.
# def car_list_view(reuqest):
#     cars = Carlist.objects.all()
#     data = {
#         'cars' : list(cars.values()),
#     }
#     data_json =  json.dumps(data)
#     # return JsonResponse(data)
#     return HttpResponse(data_json,content_type = 'application/json')



# def car_detail_view(request,pk):
#     car = Carlist.objects.get(pk=pk)
#     data = {
#         'name' : car.name,
#         'description' : car.description,
#         'active' : car.active
#     }
#     return JsonResponse(data)


@api_view(['GET','POST'])
def car_list_view(request):
    if request.method == 'GET':
        car = Carlist.objects.all()
        serializer = CarSerializer(car,many=True, context={'request': request})
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET','PUT','DELETE'])
def car_detail_view(request,pk):
    if request.method == 'GET':
        try:
            car = Carlist.objects.get(pk=pk)
        except:
            return Response({'Error':'Car Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = CarSerializer(car, context={'request': request})
        return Response(serializer.data)
    if request.method == 'PUT':
        car = Carlist.objects.get(pk=pk)
        serializer = CarSerializer(car,data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        car = Carlist.objects.get(pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

