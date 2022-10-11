from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    username = request.user.username
    print(f"Goodbye {username}, please drop by soon")
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    template_name = "djangoapp/registration.html"
    if request.method == 'POST':
        data = request.POST
        credentials = {
             'username': data['username'],
             'first_name': data['first_name'],
             'last_name': data['last_name'],
             'password': data['password']
        }

        # check if user already exists
        try:
            get_object_or_404(User, username=data['username'])
            print(f"An account for {data['username']} already exists")
            return redirect("djangoapp:index")
        except Http404:
            # create new user
            User.objects.create_user(**credentials)
            return redirect("djangoapp:index")

    return render(request, template_name, context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        results = []
        url = "http://" + request.META["HTTP_HOST"] + "/api/dealership"
        dealerships = get_dealers_from_cf(url)
        dealer_names = [dealer.short_name for dealer in dealerships]
        return render(request, 'djangoapp/index.html', context={"dealers": dealerships})

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "http://" + request.META["HTTP_HOST"] + "/api/dealership"
        dealerships = get_dealers_from_cf(url)
        dealer = [i for i in dealerships if i.id == int(dealer_id)]
        if not dealer:
            return HttpResponse(content="Unavailable", status=404)
        dealer = dealer[0] if dealer else None
        url = f'http://{request.META["HTTP_HOST"]}/api/review?dealerId={dealer_id}'
        json_result = get_dealer_by_id_from_cf(url, dealer_id)
        return render(request, 'djangoapp/dealer_details.html', context={"dealer":dealer,"reviews":json_result})

# Create a `add_review` view to submit a review
def add_review(request):
    if request.method == 'GET':
        dealer_id = request.GET.get("dealer", None)

        return render(request, 'djangoapp/add_review.html')
    if request.method == "POST":

        data = request.POST
        api_body = {"review":{"name":data["name"], "dealership":data["dealership"], "review": data["review"], "purchase": True if "purchase" in data else False, "purchase_date":data["purchase_date"], "car_make": data["car_make"], "car_model":data["car_model"], "car_year":data["car_year"]}}
        requests.post(f'http://{request.META["HTTP_HOST"]}/api/review', json=api_body)

        return redirect(f"/djangoapp/details/{data['dealership']}")
