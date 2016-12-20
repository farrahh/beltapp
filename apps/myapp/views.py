from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
# from . import models
from .models import User, Quote, Favorite

def index(request):
	return render(request, 'myapp/index.html')

def register_process(request):

	if request.method == "POST":
		result = User.objects.register(request.POST['first_name'],request.POST['last_name'],request.POST['email'],request.POST['password'], request.POST['confirm_password'])

		if result[0]==True:
			request.session['id'] = result[1].id
			print result, "***************"
			# request.session.pop('errors')
			return redirect('/quotes')
		else:

			# request.session['errors'] = result[1]
			messages.add_message(request, messages.WARNING, result[1][0])

			print result[1], "***************"
			return redirect('/')
	else:

		return redirect ('/')

def login_process(request):
	result = User.objects.login(request.POST['email'],request.POST['password'])

	if result[0] == True:
		request.session['id'] = result[1][0].id
		return redirect('/quotes')
	else:
		messages.add_message(request, messages.WARNING, result[1][0])
		return redirect('/')

def users(request, id):
	if not 'id' in request.session :
		return redirect('/')
	else:
		session = request.session['id']
		loggedInUser = User.objects.filter(id=session)
		user = User.objects.filter(id=session)
		userName = user[0].first_name

		allQuotes = Quote.objects.filter(user__id=id).order_by('-created_at')
		quoteCount = allQuotes.count()

		data = {
			'allQuotes': allQuotes,
			'userName': userName,
			'quoteCount': quoteCount,
			'loggedInUser': loggedInUser[0].first_name,
			'quotePosterUserName': allQuotes[0].user.first_name,
			'sessionID': session
		}

	return render(request, "myapp/users.html", data)


	# -------login/registration--------

def quotes(request):
	if not 'id' in request.session :
		return redirect('/')
	else:
		session = request.session['id']
		loggedInUserObject = User.objects.filter(id=session)
		allQuotes = Quote.objects.all().exclude(favoritequote__user__id=session).order_by('-created_at')
		quotePosterUserObject = User.objects.filter(id=session)
		quotePosterUserName = quotePosterUserObject[0].first_name
		favQuote = Favorite.objects.all().filter(user__id=session)
# print favQuote, "*"*300


		data = {
			'allQuotes': allQuotes,
			'quotePosterUserName': quotePosterUserName,
			'quotePosterUserID': session,
			'loggedInUser': loggedInUserObject[0].first_name,
			'favQuotes': favQuote
		}

	return render(request, "myapp/quotes.html", data)

def add_quote(request):
	res = Quote.objects.create_quote(request.POST, request.session['id'])
	return redirect ('/quotes')

def add_fav(request, id):
	Favorite.objects.add_fav(id, request.session['id'])

	return redirect('/quotes')

def remove_fav(request, id):
	res = Favorite.objects.filter(quote_id=id).delete()
	print res, "^"*300
	return redirect ('/quotes')

def logout(request)	:
	del request.session['id']
	return redirect ('/')
