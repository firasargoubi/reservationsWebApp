from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from .models import Units, Client,Garage
from datetime import datetime
from django.template import loader
from django.db.models import Prefetch
from django.urls import reverse
import yagmail

def calendar(request) :
    if (Garage.objects.all().count() == 0) :
        for i in range(1,9) :
            garage = Garage(occupied = False,number = i,code = 69420)
            garage.save()
            print(garage)
    
    if (Units.objects.all().count() == 0) :
        unit = Units(short = "FU",name = "FirstUnit")
        unit.save()
        unit2 = Units(short = "SU", name = "SecondUnit")
        unit2.save()
    
    context = {
        'units' : Units.objects.all().values(),
    }
    
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context, request))

def make_reservation(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        unit = data.get('unit')
        username = data.get('username')
        email = data.get('email')
        isAvailable, garageNum = is_available(start_date, end_date)
        isFraud,idFraud = is_fraud(start_date,end_date,unit)
        if isFraud or isAvailable:
            
            
            message = "Reservation made successfully, an email with the details has been sent!" if not isFraud else "Your reservation is still on hold, we will contact you for more informations ."
            # Create reservation
            client = Client(username = username,email=email,
                            start_date = start_date, end_date = end_date,unit = unit,
                            garage_num = garageNum)
            if isFraud :
                clientOriginal = Client.objects.get(id=idFraud)
                clientOriginal.garage_num =  0
                client.invalid = True
                clientOriginal.garage_num =  0
                clientOriginal.invalid = True
                clientOriginal.save()
                
            client.save()
            sendingEmailConfirmation(client,isFraud)
            return JsonResponse({'success':not isFraud, 'message': message})
            
        else:
            return JsonResponse({'success': False, 'message': 'Slot not available'})
            #Add a email bot to send an email to the admin about the fact that a Customer doesn't have a Garage 
    else:
        return JsonResponse({'error': 'Invalid request'})

def timeline(request) :
    clients = Client.objects.all().values()
    context = {
        'clients': clients,
        'range' : range(1,Garage.objects.all().count()+1)
    }
    return render(request, 'timeline.html', context)

def delete_page(request,id) :
    client = Client.objects.get(id=id)
    context = {
        'client': client
    }
    sendingEmailDeletion(client)
    client.delete()
    
    return render(request, 'delete_page.html', context)

def delete_client(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            client = Client.objects.get(id=data.get('id'))
            sendingEmailDeletion(client)
            client.delete()
            
            return JsonResponse({'success': True, 'message': 'Client deleted successfully, please refresh the page.'})
        except Client.DoesNotExist:
            print("Meh")
            return JsonResponse({'success': False, 'message': 'Client not found.'})
        except Exception as e:
            print("Boo",e)
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        print("Huh")
        return JsonResponse({'error': 'Invalid request'})

def validate_user(request) :
    if request.method == 'POST' :
        data = json.loads(request.body)
        id = data.get('id')
        client = Client.objects.get(id=id)
        key = is_available(client.start_date, client.end_date)
        isFraud,num = is_fraud(client.start_date, client.end_date, client.unit)
        if not key[0]:
            return JsonResponse({'success': False, 'message': 'There is no place for the client'})
        elif isFraud :
            return JsonResponse({'success': False, 'message': 'Adding this client would make the reservation fraudulent'})
        client.invalid=False
        client.garage_num=key[1]
        client.save()
        sendingEmailConfirmation(client,False)
        return JsonResponse({'success': True,'message' : "The user is now validated, please refresh the page"})
    
def invalidate_user(request) :
    if request.method == 'POST' :
        data = json.loads(request.body)
        id = data.get('id')
        client = Client.objects.get(id=id)
        client.invalid=True
        client.garage_num=0
        client.save()
        return JsonResponse({'success': True,'message' : "The user is now invalidated, please refresh the page"})

"Helper functions"
def is_duplicate(username,email,unit,start_date,end_date) :
    for client in Client.objects.all().values() :
        if ((client["username"].lower() == username.lower() or client["email"].lower() == email.lower()) and 
            client["unit"].lower() == unit.lower() and 
            client["start_date"] == start_date and 
            client["end_date"] == end_date ):
            return True
    return False

def is_fraud(start_date,end_date,unit) :
    for client in Client.objects.all().values() :
        if (client["start_date"] == start_date and 
            client["end_date"] == end_date and
            client["unit"] == unit and
            client["garage_num"] !=0 ):
            return [True,client["id"]]
    return [False,0]

def is_available(start_date,end_date) :
    newDateS = datetime.strptime(start_date,"%Y-%m-%d")
    newDateE = datetime.strptime(end_date,"%Y-%m-%d")
    for i in range(1,9) :
        seen = False
        if Client.objects.count() == 0 :
            return [True,1]
        search = Client.objects.filter(garage_num = i).values()
        for client in search :
            curS = datetime.strptime(client["start_date"],"%Y-%m-%d")
            curE =  datetime.strptime(client["end_date"],"%Y-%m-%d")
            if curS <= newDateS <= curE or curS <= newDateE <= curE :
                seen = True
                break
        if seen == False :
            return [True,i]
    return [False,0]   

def update_clients_and_garage():
    today = datetime.now().strftime("%Y-%m-%d")
    for client in Client.objects.all().values() :
        if client.start_date == today :
            sendingEmailStartDate(client)
        elif client.end_date == today :
            sendingEmailEndDate(client)
            client.delete()      

def sendingEmailConfirmation(client, isFraud):
    yag = yagmail.SMTP("garageconfirmationkey@gmail.com", "nhpi xxxu eqkc ylzm")

    try:
        if not isFraud:
            subject = "Garage Reservation Confirmation"
            delete_reservation_url = reverse('delete_reservation', kwargs={'id': client.id})
            contents = """
                <html>
                <body>
                    <p>Dear {0},</p>
                    <p>Thank you for booking your stay with us! We are pleased to confirm your reservation details:</p>
                    <p>Unit: {1}</p>
                    <p>Check-in Date: {2}</p>
                    <p>Check-out Date: {3}</p>
                    <p>If you need to make any changes or have any questions, please don't hesitate to contact us.</p>
                    <p>To delete your reservation, click <a href="{4}">here</a>.</p>
                    <p>Best regards,</p>
                    <p>Your Garage Team</p>
                </body>
                </html>
            """.format(client.username, client.unit, client.start_date, client.end_date, delete_reservation_url)
        else:
            return ''
        yag.send(to=client.email, subject=subject, contents=contents)
    except Exception as e:
        print("Error sending email: {0}".format(e))

def sendingEmailDeletion(client):
    yag = yagmail.SMTP("garageconfirmationkey@gmail.com", "nhpi xxxu eqkc ylzm")

    try:
        subject = "Garage Reservation Deletion"
        contents = """
            <html>
            <body>
                <p>Dear {0},</p>
                <p>We regret to inform you that your reservation has been canceled.</p>
                <p>Unit: {1}</p>
                <p>Check-in Date: {2}</p>
                <p>Check-out Date: {3}</p>
                <p>If you have any questions or concerns, please don't hesitate to contact us.</p>
                <p>Best regards,</p>
                <p>Your Garage Team</p>
            </body>
            </html>
        """.format(client.username, client.unit, client.start_date, client.end_date)
        yag.send(to=client.email, subject=subject, contents=contents)
        print("Deletion email sent to {0}".format(client.email))
    except Exception as e:
        print("Error sending email: {0}".format(e))

def sendingEmailStartDate(client):

    yag = yagmail.SMTP("garageconfirmationkey@gmail.com", "nhpi xxxu eqkc ylzm")

    try:
        subject = "Garage Reservation Reminder"
        contents = """
            <html>
            <body>
                <p>Dear {0},</p>
                <p>This is a friendly reminder that your garage reservation starts today!</p>
                <p>Reservation Details:</p>
                <p>Unit: {1}</p>
                <p>Check-in Date: {2}</p>
                <p>Check-out Date: {3}</p>
                <p>Garage Number: {4}</p>
                <p>Garage Code: {5}</p>
                <p>Please use the provided garage code to access your assigned garage.</p>
                <p>If you have any questions or concerns, please don't hesitate to contact us.</p>
                <p>Best regards,</p>
                <p>Your Garage Team</p>
            </body>
            </html>
        """.format(client.username, client.unit, client.start_date, client.end_date, client.garage_num, garage.code)
        yag.send(to=client.email, subject=subject, contents=contents)
        print(f"Reservation reminder email sent to {client.email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def sendingEmailEndDate(client):

    yag = yagmail.SMTP("garageconfirmationkey@gmail.com", "nhpi xxxu eqkc ylzm")

    try:
        subject = "Garage Reservation Reminder"
        contents = """
            <html>
            <body>
                <p>Dear {0},</p>
                <p>This is a friendly reminder that your garage reservation starts today!</p>
                <p>Reservation Details:</p>
                <p>Unit: {1}</p>
                <p>Check-in Date: {2}</p>
                <p>Check-out Date: {3}</p>
                <p>Garage Number: {4}</p>
                <p>Garage Code: {5}</p>
                <p>Please use the provided garage code to access your assigned garage.</p>
                <p>If you have any questions or concerns, please don't hesitate to contact us.</p>
                <p>Best regards,</p>
                <p>Your Garage Team</p>
            </body>
            </html>
        """.format(client.username, client.unit, client.start_date, client.end_date, client.garage_num, garage.code)
        yag.send(to=client.email, subject=subject, contents=contents)
        print(f"Reservation reminder email sent to {client.email}")
    except Exception as e:
        print(f"Error sending email: {e}")