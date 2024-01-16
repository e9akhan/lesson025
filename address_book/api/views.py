"""
    Module name :- views
    Method(s) :- contact(), contact_with_pk()
"""

import json
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from book.models import Contact


# Create your views here.
@csrf_exempt
def contact(request):
    """
    Accept GET and POST methods for list of data.
    """

    if request.method == "POST":
        body = json.loads(request.body.decode("utf8"))
        user = User.objects.get(id=body["user"])

        user_contact = Contact.objects.create(
            user=user,
            name=body["name"],
            email=body.get("email", []),
            phone_no=body["phone_no"],
            address=body.get("address", []),
        )

        user_contact.save()
        return JsonResponse({"message": "Created"}, safe=False)

    json_data = json.loads(serializers.serialize("json", Contact.objects.all()))
    return JsonResponse({"items": json_data}, safe=False)


@csrf_exempt
def contact_with_pk(request, pk):
    """
    Function for individual data.
    """

    if request.method == "PUT":
        body = json.loads(request.body.decode("utf8"))
        user_contact = Contact.objects.get(pk=pk)

        user = User.objects.get(pk=body["user"])

        user_contact.user = user
        user_contact.name = body["name"]
        user_contact.email = body["email"]
        user_contact.phone_no = body["phone_no"]
        user_contact.address = body["address"]

        user_contact.save()

        return JsonResponse({"message": "Updated"}, safe=False)

    if request.method == "PATCH":
        body = json.loads(request.body.decode("utf8"))
        user_contact = Contact.objects.get(pk=pk)

        if "user" in body:
            user = User.objects.get(pk=body["user"])
            user_contact.user = user

        if "name" in body:
            user_contact.name = body["name"]

        if "email" in body:
            user_contact.email = body["email"]

        if "phone_no" in body:
            user_contact.phone_no = body["phone_no"]

        if "address" in body:
            user_contact.address = body["address"]

        user_contact.save()

        return JsonResponse({"message": "Updated"}, safe=False)

    if request.method == "DELETE":
        user_contact = Contact.objects.get(pk=pk)
        user_contact.delete()

        return JsonResponse({"message": "Deleted"}, safe=False)

    user_contact = Contact.objects.filter(pk=pk)
    json_data = json.loads(serializers.serialize("json", user_contact))
    return JsonResponse({"item": json_data}, safe=False)
