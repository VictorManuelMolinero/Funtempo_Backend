from api.models import Schedule
from django.http.response import JsonResponse
from rest_framework import status
from api.serializers import ScheduleSerializer
from rest_framework.views import APIView

class ScheduleController(APIView):

    #Method to get all schedules of the logged user
    def get(self, request, username, format=None):

        #Filter them using the username and order them from soonest to latest starting hour
        schedules = Schedule.objects.filter(username=username).order_by('starting_hour')

        if not schedules:
            return JsonResponse({"error": "Schedules not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(serializer.data, safe=False)

    '''Method to get all the schedules from the database
    It wasn't used, but i added it because it's a default CRUD method'''
    def getAll(self, format=None):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    #Method to add a schedule in the database
    def post(self, request, format=None):
        #Serialize it so it can be saved in the database
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
    
    #Method to update a schedule in the database
    def put(self, request, schedule_id, format=None):
        #Search it in the database using it's id
        try:
            schedule = Schedule.objects.get(pk=schedule_id)
        except Schedule.DoesNotExist:
            return JsonResponse({"error": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)

        #Update the object with the new data
        schedule.starting_hour = request.data.get('starting_hour')
        schedule.finishing_hour = request.data.get('finishing_hour')
        schedule.description = request.data.get('description')

        schedule.save()
        
        return JsonResponse({'message': 'The schedule was updated successfully'}, 
                            status=status.HTTP_200_OK, safe=False)
    
    #Method to delete a schedule from the database
    def delete(self, request, format=None):
        try:
            schedule_id = request.data.get('schedule_id')
            #Search the schedule using it's id
            schedule = Schedule.objects.get(pk=schedule_id)
        except Schedule.DoesNotExist:
            return JsonResponse({"error": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        
        schedule.delete()
        return JsonResponse({'message': 'The schedule was deleted successfully'}, 
                status=status.HTTP_200_OK, safe=False)
