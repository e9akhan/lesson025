from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from book.models import Contact

# Create your views here.
@csrf_exempt
def contact(request):
    if request.method == 'GET':
        json_data = serializers.serialize('json', Contact.objects.all())
        return JsonResponse({'items': json_data}, safe=False)
    
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf8'))
        print(body)

        user = User.objects.get(
            id=body['user']
        )
        
        contact = Contact.objects.create(
            user = user,
            name = body['name'],
            email = body.get('email', []),
            phone_no = body['phone_no'],
            address = body.get('address', [])
        )

        contact.save()
        return JsonResponse({'message': 'Created'}, safe=False)

@csrf_exempt
def contact_with_pk(request, pk):
    if request.method == 'GET':
        contact = Contact.objects.get(
            pk=pk
        )
        json_data = json.dumps(contact)
        return JsonResponse({'item': json_data}, safe=False)

    if request.method == 'PUT':
        body = json.loads(request.body.decode('utf8'))
        print(body)
        contact = Contact.objects.get(
            pk=pk
        )

        user = User.objects.get(
            pk=body['user']
        )

        contact.user = user
        contact.name = body['name']
        contact.email = body['email']
        contact.phone_no = body['phone_no']
        contact.address = body['address']

        contact.save()

        return JsonResponse({'message': 'Updated'}, safe=False)

    if request.method == 'PATCH':
        body = json.loads(request.body.decode('utf8'))
        contact = Contact.objects.get(
            pk=pk
        )

        if 'user' in body:
            user = User.objects.get(
            pk=body['user']
        )
            contact.user = user

        if 'name' in body:
            contact.name = body['name']

        if 'email' in body:
            contact.email = body['email']

        if 'phone_no' in body:
            contact.phone_no = body['phone_no']

        if 'address' in body:
            contact.address = body['address']

        contact.save()

        return JsonResponse({'message': 'Updated'}, safe=False)
    
    if request.method == 'DELETE':
        contact = Contact.objects.get(
            pk=pk
        )
        contact.delete()

        return JsonResponse({'message': 'Deleted'}, safe=False)
    
def contact_filter(request, category):
    print(category)
    contacts = Contact.objects.all()
    contacts = sorted(contacts, key=lambda contact: contact.get(category))

    json_data = serializers.serialize('json', contacts)
    return JsonResponse({'items': json_data}, safe=False)