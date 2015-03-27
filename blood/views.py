import json
from django.core.mail import send_mail
from django.core import serializers
from django.utils.timezone import now as utcnow
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from datetime import datetime as dt
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from blood.models import Choice, Question, Donor, Recepient, Hospital, Camp, Link, Post, Story,Notification, User
from django.contrib.auth.decorators import login_required

emailil="bloodconnect14@gmail.com"

@login_required
def view_request(request,requestID):
	request_list=Recepient.objects.get(id=requestID)
	context={'requestit':request_list}
	return render(request,'blood/view_request.html',context)
@login_required
def view_request_thanks(request,requestID):
	request_list=Recepient.objects.get(id=requestID)
	val=str(request.user)
	val1=str(request.user.email)
	body="Mr "+val+" wants to donate blood to your need.\n\nDetails:\n"
	body+="Name: "+val1+"\nEmail: "+val1+"\n"
	body+="\nKindly contact the user in case of need\n\nRegards,\nBloodConnect\n"
	subject="Regarding Blood Donation at BloodConnect"
	mailit=[]
	mailit.append(request_list.email)
	send_mail(subject, body, emailil,mailit)
	context={'requestit':request_list}
	return render(request,'blood/view_request_thanks.html',context)

def main(request):
	return render(request,'blood/main.html')
@login_required
def send_email1(request):
	email=request.user.email
	rst=Recepient.objects.filter(email=email)
	bggroup=rst[0].bggroup
	don=Donor.objects.filter(bggroup=bggroup)
	for i in don:
		to_addr=i.email
		body="You can save many lives"
		subject="Regarding Blood Donation Request"
		mailit=[]
		mailit.append(i.email)
		send_mail(subject, body, email,mailit)
	return render(request,'blood/send_email1.html')
@login_required
def index(request):
    if request.user.is_authenticated():
	user=request.user.username
	email = request.user.email
    	context = {'user': user, 'email': email}
    return render(request, 'blood/index.html', context)

@login_required
def donor(request):
	order_list = Donor.objects.all().order_by('name')
	print order_list
	context = {'order_list': order_list}
	return render(request, 'blood/donor.html', context)

@login_required
def share(request):
	user = request.user.username
	new_var=Story.objects.filter(suser__id=request.user.id)
	order_list = Story.objects.all().order_by('tag')
	context = {'order_list': order_list,'user': user, 'new_var':new_var}
	return render(request, 'blood/share.html', context)

@login_required
def view_story(request,story_id):
	order_list = Story.objects.get(id=story_id)
	context = {'order_list': order_list}
	return render(request, 'blood/view_story.html', context)
#	order_list = Story.objects.
@login_required
def home(request):
	if request.user is not None:
		cu=request.user.profile
		cu.is_chat_user=True
		cu.last_accessed=utcnow()
		cu.save()
		requests = Recepient.objects.all()
		context = {'requests':requests}
	return render(request, 'blood/home.html',context);
@login_required
def camp_donate(request,campID):
	query = Camp.objects.get(id=campID)
	st = query.sdate+"T00:00:00.000-08:00"#.split("/")
	en = query.edate+"T00:00:00.000-08:00"
	form=Link()
	form.cid=campID
	form.uid=request.user.id
	form.flag=1
	form.guser=request.user
	form.save()
	context = {'st':st,'en':en,'query':query}
	return render(request,'blood/camp_donate.html',context)

@login_required
def todaycamp(request):
	camp_list=Camp.objects.all()
	campit=[]
	flag={}
	for camp in camp_list:
		sdate1=dt.strptime(camp.sdate,'%Y-%m-%d').date()
		edate1=dt.strptime(camp.edate,'%Y-%m-%d').date()
		if(sdate1<=datetime.date.today() and edate1>=datetime.date.today()):
			campit.append(camp)
		ln=Link.objects.filter(cid=camp.id).filter(guser=request.user)
		if len(ln)>0:
		 	flag[camp.id]=1
		else:
		 	flag[camp.id]=0
		#print sdate1,edate1,datetime.date.today()
		#camp_list=Camp.objects.filter(datetime.strptime(sdate,'%Y-%m-%d')<=datetime.date.today()).filter(datetime.strptime(edate,'%Y-%m-%d')>=datetime.date.today())
	email=request.user
	context={'camp_list':campit, 'email':email,'flag':flag}
	return render(request,'blood/todaycamp.html', context)
def faqs(request):
	return render(request, 'blood/faqs.html');
def feedback(request):
	return render(request, 'blood/feedback.html');
def contact(request):
	return render(request, 'blood/contact.html');
def about(request):
	return render(request, 'blood/about.html');

@login_required
def drive(request):
	if request.user.is_authenticated:
		user = request.user.username
	#Either use it as a string or pdf ???
	query = Camp.objects.filter(email=request.user.email)
	context = {'user':user,'q':query}
	return render(request, 'blood/drive.html',context)

@login_required
def drive_list(request,driveID):
	user = request.user.username
	#Either use it as a string or pdf ???
	cdetails = Camp.objects.get(id=int(driveID))
	query = Link.objects.filter(cid=int(driveID))
	corg=cdetails.uid
	corg=User.objects.get(id=corg)
	print query
	dquery = []
	a = []
	b=[]
	ldquery = 0
	emailit=[]
	for i in query:
		#print i.user.get(pk=1)
		a.append(i.guser)
		dquery.append(a)
		a=[]
		#print i.user.objects.all()
		#us=i.user.get(pk=1)
		#us=us.id
		us=User.objects.get(id=i.uid)
	#	print us
	#	queryit=User.objects.get(id=us)
		b.append(us.email)
		emailit.append(b)
		b=[]
	#print json.dumps(dquery)
	context = {'user':user,'q':query,'corg':corg,'cdetails':cdetails,'tdon':len(query),'dquery':json.dumps(dquery),'emailit':json.dumps(emailit)}
	return render(request, 'blood/drive_list.html',context)

@login_required
def calendar(request):
	if request.user.is_authenticated:
		user = request.user.username
	#Query To get the start and end date of camp Assuming one element
	query = Camp.objects.filter(email=request.user.email)
	st=""
	en=""
	if len(query)>0:
		st = query[0].sdate+"T00:00:00.000-08:00"#.split("/")
		en = query[0].edate+"T00:00:00.000-08:00"#.split("/")
	context = {'user':user , 'st':st,'en':en}
	return render(request, 'blood/calendar.html',context)


@login_required
def putstory(request):
	if request.method=='POST':
		form=Story()
		form.tag=request.POST['description']
		form.story=request.POST['bio']
		form.save()
		form.suser.add(request.user)
		return render(request, 'blood/putstory_thanks.html')
	return render(request,'blood/putstory.html')

@login_required
def putstory_thanks(request):
	return render(request, 'blood/putstory_thanks.html')

@login_required
def stry(request):
	order_list = Story.objects.all().order_by('tag')
	context = {'order_list': order_list}
	return render(request, 'blood/stry.html', context)

@login_required
def requestblood_form(request):
	if request.user.is_authenticated:
		user = request.user.username
	query = Recepient.objects.filter(email=request.user.email)
	if len(query)==1:
		query = query[0]
	context = {'user':user,'query':query}
	if request.method=='POST':
		query = Recepient.objects.filter(email=request.user.email)
		if len(query)==1:
			query=query[0]
			query.name=request.POST['name']
			query.address=request.POST['address']
			query.age=request.POST['age']
			query.bggroup=request.POST['bg']
			query.bgunits=request.POST['bunits']
			query.contact=request.POST['contact']
			query.lat1=request.POST['latitude']
			query.long1=request.POST['longitude']
			body="You have saved many lives. Thank You "+query.name+" for your donation.\n"
			body+="You can find list of all interested donors on this map "+"bloodconnect.bluemix.net/blood/donor_list\n"
			body+="\nDetails:\n"
			body+="Name: "+query.name+"\n"+"Blood Group: "+query.bggroup+"\n"+"Blood Units: "+str(query.bgunits)
			body+="\n"+"Contact: "+str(query.contact)+"\nAddress: "+query.address+"\n\nRegards,\nBloodConnect"
			subject="Regarding Blood Donation Request at BloodConnect"
			mailit=[]
			mailit.append(request.user.email)
			send_mail(subject, body, emailil,mailit)
			query.save()
			return HttpResponseRedirect('/blood/donor_list/')
		else:
			form=Recepient()
			form.name=request.POST['name']
			form.address=request.POST['address']
			form.age=request.POST['age']
			form.bggroup=request.POST['bg']
			form.bgunits=request.POST['bunits']
			form.contact=request.POST['contact']
			form.lat1=request.POST['latitude']
			form.long1=request.POST['longitude']
			form.email=request.user.email
			body="You have saved many lives. Thank You "+form.name+" for your donation.\n"
			body+="You can find list of all interested donors on this map "+"bloodconnect.bluemix.net/blood/donor_list\n"
			body+="\nDetails:\n"
			body+="Name: "+form.name+"\n"+"Blood Group: "+form.bggroup+"\n"+"Blood Units: "+str(form.bgunits)
			body+="\n"+"Contact: "+str(form.contact)+"\nAddress: "+form.address+"\n\nRegards,\nBloodConnect"
			subject="Regarding Blood Donation Request at BloodConnect"
			form.save()
			form.user.add(request.user)
			return HttpResponseRedirect('/blood/donor_list')
	return render(request, 'blood/requestblood_form.html',context)

@login_required
def donor_list(request):
	if request.user.is_authenticated:
		user = request.user.username
	query = Recepient.objects.filter(email=request.user.email)
	if(len(query)!=0):
		donor = Donor.objects.filter(bggroup = query[0].bggroup )
	else:
		donor=[]
	if(len(query)!=0):
		rlat = query[0].lat1
		rlong = query[0].long1
		radd = query[0].address
	else:
		rlat=17.3660
		rlong=78.4760
		radd="Hyderabad, Andhra Pradesh, India"
	ddetails = []
	a = []
	b = []
	final = []
	for i in donor:
		a.append(i.name)
		b.append(i.name)
		a.append(i.email)
		b.append(i.email)
		a.append(i.address)
		b.append(i.address)
		a.append(i.contact)
		b.append(i.contact)
		a.append(i.age)
		b.append(i.age)
		a.append(i.bgunits)
		b.append(i.bgunits)
		ddetails.append(b)
		a.append(i.lat1)
		a.append(i.long1)	
		final.append(a)
		a=[]
		b=[]
	context = {'user':user,'details':ddetails,'rlat':rlat,'rlong':rlong,'radd':radd,'final1':json.dumps(final)}
	return render(request, 'blood/donor_list.html',context)	
	
@login_required
def bloodcamp_list(request):
	flagit=0
	if request.user.is_authenticated:
		user = request.user.username
	query = Camp.objects.filter(email=request.user.email)
	if(len(query)==0):
		camp=Camp.objects.all()
		flagit=1
		rlat=17.385044
		rlong=78.486671
		radd = ""

	camp = Camp.objects.all()
	if(flagit==0):
		rlat = query[0].lat1
		rlong = query[0].long1
		radd = query[0].address
	ddetails = []
	a = []
	b = []
	final = []
	for i in camp:
		a.append(i.name)
		b.append(i.name)
		a.append(i.email)
		b.append(i.email)
		a.append(i.address)
		b.append(i.address)
		a.append(i.contact)
		b.append(i.contact)
		ddetails.append(b)
		a.append(i.lat1)
		a.append(i.long1)	
		final.append(a)
		a=[]
		b=[]
	context = {'user':user,'details':ddetails,'rlat':rlat,'rlong':rlong,'radd':radd,'final1':json.dumps(final)}
	return render(request, 'blood/bloodcamp_list.html',context)

def requestblood_thanks(request):
	return render(request,'blood/requestblood_thanks.html')

def donateblood_thanks(request):
	return render(request,'blood/donateblood_thanks.html')

@login_required
def bloodcamp(request):
	query=Camp.objects.all()
	if(query):
		flagit=0
	else:
		flagit=1
	context={'flagit':flagit}
	return render(request,'blood/bloodcamp.html',context)

def camps_detail(request):
	tot_list=Camp.objects.all()
	selected_camps=Link.objects.filter(guser=request.user)
	going_list=[]
	camp_list=[]
	going=[]
	for i in selected_camps:
		going.append(int(i.cid))
		going_list.append(Camp.objects.get(id=i.cid))
	for i in tot_list:
		if i.id not in going:
			camp_list.append(i)
	email=request.user
	context={'camp_list':camp_list, 'email':email ,'going_list':going_list,'going':going}
	return render(request,'blood/camps_detail.html', context)

@login_required
def bloodcamp_form(request):
	if request.user.is_authenticated:
		user = request.user.username
	if request.method=='POST':
		form=Camp()
		form.name=request.POST['name']
		form.address=request.POST['address']
		form.contact=request.POST['contact']
		form.lat1=request.POST['latitude']
		form.long1=request.POST['longitude']
		valit= datetime.date.today()
		form.cdate=valit
		#print request.POST['sdate']
		form.sdate=request.POST['sdate']
		form.edate=request.POST['edate']
		form.email=request.user.email
		form.uid=request.user.id
		form.save()
		return HttpResponseRedirect('/blood/bloodcamp_list')
	context = {'user':user}
	return render(request, 'blood/bloodcamp_form.html',context)

def bloodcamp_form_thanks(request):
	return render(request,'blood/bloodcamp_form_thanks.html');

def camp_post(request,campID):
	camplist=Camp.objects.get(id=campID)
	uid=camplist.uid
	userit=User.objects.get(id=uid)
	postit=Post.objects.filter(campid=campID)
	ait=[]
	for post in postit:
		valit=post.uid
		value=User.objects.get(id=valit)
		print value
		ait.append(value)
	print ait
	context={'campID':campID, 'camplist':camplist, 'postit':postit, 'userit':userit, 'lit':zip(postit,ait)}
	return render(request,'blood/camp_post.html',context)

def store_camp_post(request,campID):
	if request.method=='POST':
		form=Post()
		form.comment=request.POST['comment']
		form.campid=campID
		form.uid=request.user.id
		form.save()
	return HttpResponseRedirect('/blood/camp_post/'+(campID)+'/')
#return render(request,'blood/camp_post.html/{{campID}}')

@login_required
def donate_blood(request):
	if request.user.is_authenticated:
		user = request.user.username
	query = Donor.objects.filter(email=request.user.email)
	if len(query)==1:
		query = query[0]
	context = {'user':user,'query':query}
	if request.method=='POST':
		query = Donor.objects.filter(email=request.user.email)
		if len(query)==1:
			query=query[0]
			query.name=request.POST['name']
			query.address=request.POST['address']
			query.age=request.POST['age']
			query.bggroup=request.POST['bg']
			query.bgunits=request.POST['bunits']
			query.contact=request.POST['contact']
			query.lat1=request.POST['latitude']
			query.long1=request.POST['longitude']
			body="You have saved many lives. Thank You "+query.name+" for your donation.\n\n"+"Details:\n"
			body+="Name: "+query.name+"\n"+"Blood Group: "+query.bggroup+"\n"+"Blood Units: "+str(query.bgunits)
			body+="\n"+"Contact: "+str(query.contact)+"\nAddress: "+query.address+"\n\nRegards,\nBloodConnect"
			subject="Regarding Blood Donation at BloodConnect"
			mailit=[]
			mailit.append(request.user.email)
			send_mail(subject, body, emailil,mailit)
			query.save()
		else:
			form=Donor()
			form.name=request.POST['name']
			form.address=request.POST['address']
			form.age=request.POST['age']
			form.bggroup=request.POST['bg']
			form.bgunits=request.POST['bunits']
			form.contact=request.POST['contact']
			form.lat1=request.POST['latitude']
			form.long1=request.POST['longitude']
			form.email=request.user.email
			body="You have saved many lives. Thank You "+form.name+" for your donation.\n\n"+"Details:\n"
			body+="Name: "+form.name+"\n"+"Blood Group: "+form.bggroup+"\n"+"Blood Units: "+str(form.bgunits)
			body+="\n"+"Contact: "+str(form.contact)+"\nAddress: "+form.address+"\n\nRegards,\nBloodConnect"
			subject="Regarding Blood Donation at BloodConnect"
			mailit=[]
			mailit.append(form.email)
			send_mail(subject, body, emailil,mailit)
			form.save()
			form.user.add(request.user)
		return render(request, 'blood/donateblood_thanks.html')
	return render(request, 'blood/donate_blood.html',context)

def faqs(request):
	return render(request, 'blood/faqs.html');
def recepient(request):
	order_list = Recepient.objects.all().order_by('name')
	context = {'order_list:': order_list}
	return render(request, 'blood/recepient.html', context)

def hospital(request):
	order_list = Hospital.objects.all().order_by('name')
	context = {'order_list': order_list}
	return render(request, 'blood/hospital.html', context)

def camp(request):
	order_list = Camp.objects.all().order_by('name')
	context = {'order_list': order_list}
	return render(request, 'blood/camp.html', context)

def link(request):
	order_list = Link.objects.all().order_by('cid')
	context = {'order_list': order_list}
	return render(request, 'blood/link.html', context)

def post(request):
	order_list = Post.objects.all().order_by('user')
	context = {'order_list': order_list}

def story(request):
	order_list = Story.objects.all().order_by('user')
	context = {'order_list': order_list}

def Notification(request):
	order_list = Notification.objects.all().order_by('did')
	context = {'order_list': order_list}

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'blood/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
