from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from playing_with_electoral_bond import settings
from django.core.mail import send_mail,EmailMessage 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token 
from authentication.models import ImageUpload
from django.views.decorators.csrf import csrf_exempt
from authentication.models import ACModel, Comment
from django.utils import timezone
import os
# Create your views here.

def sign_in(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        
        if username != "" and  password != "":
            user = authenticate(username = username, password = password)

            if user is not None and user.is_active == True:
                login(request,user)
                request.session["user_name"] = username
                session_id = request.session.session_key
                messages.success(request,'You have loged in successfully')
                return redirect('/user/{}/'.format(session_id))
                #return redirect('home')


            else:
                messages.error(request,'Check your id and Password or please activate your account.')
                return redirect('sign_in')
        
        else:
            messages.error(request,'these field can not be empty.')
            return redirect('sign_in')

    return render(request,'authentication/sign_in.html',{'is_error': True} )

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get("username")
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass']
        confirm_password = request.POST['conf_pass']

        if username != "" and fname != "" and lname != "" and email != "" and password != "":
            if password == confirm_password:
                if User.objects.filter(username = username) or User.objects.filter(email = email):
                    messages.error(request,'username is already exsit')
                    return render(request,'sign_up')

                myuser = User.objects.create_user(username,email,password)
                myuser.first_name = fname
                myuser.last_name = lname
                myuser.is_active = False
                myuser.save()
            

                # subject = "Welcome To Playing With Electoral Bond Website"
                # message = "Hello " + myuser.first_name + "\n" + "Welcome to  playing with electoral bond website. \n thank for visting our Website \n We have sent you confirmation mail in order to validate user account.\n please click on the below link to activate your account. \n\n Thank You  \n Team Website"
                from_email = settings.EMAIL_HOST_USER
                to_mail = myuser.email
                # send_mail(subject,message,from_email,to_mail, fail_silently = False)

                current_site = get_current_site(request)  
                mail_subject = 'Activation link has been sent to your email id'  
                message = render_to_string('acc_active_email.html', {  
                    'myuser': myuser,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),  
                    'token':account_activation_token.make_token(myuser),  
                })  
                email = EmailMessage(  
                            mail_subject, message, from_email, to=[to_mail]  
                )  
                email.send(fail_silently = False)

                success = True
                messages.success(request,"you will recieve the confirmation mail in order to activate your account.plaese check your email.Thank You !")  
                return render(request,'authentication/sign_in.html',{'check': success})

            else:
                messages.error(request,"Entered Password did not Matched !")
                return redirect('sign_up')

        else:
            messages.error(request,"Fields can not be Empty!")
            return redirect('sign_up')
                   #welcome Email
                


    return render(request,'authentication/sign_up.html')

def activate(request, uidb64, token):    
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        myuser = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        myuser = None  
    if myuser is not None and account_activation_token.check_token(myuser, token):  
        myuser.is_active = True  
        myuser.save()  
        login(request,myuser)
        return redirect('home')  
    else:  
        return HttpResponse('Activation link is invalid!')

def sign_out(request):
    logout(request)
    request.session.flush()
    return redirect('home')

def saveArticle(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST['title']
            subTitle = request.POST['sub_title']
            author_name = request.POST['authorName']
            if author_name == "":
                author_name = request.user.first_name+" "+ request.user.last_name 
            content = request.POST['content']
            current_user = request.user
            dateTime = timezone.localtime(timezone.now())
            if title != "" and content != "":
                ACModel.objects.create(user=current_user,title=title,subtitle=subTitle,author=author_name,content=content,date_time=dateTime)
                # x= ACModel.objects.all()
                # print(x)
                messages.error(request,'Thank You for sharing your article. it is under review. it will take some time to reflect on page.')
                redirect('view_articles')
            else:
                messages.error(request,'Write Your Article!')
                redirect('view_articles')

    else:
        return redirect('sign_in')

    return redirect('view_articles')

def add_comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user 
            comment = request.POST['comment']
            dateTime=timezone.localtime(timezone.now())
            # print(comment)
            if comment != "":
                Comment.objects.create(user=user,comment=comment,date_time=dateTime)
                return redirect('view_articles')
            else:
                return redirect('sign_up')
    else:
        return redirect('sign_in')

def update_comment(request):
    if request.method == 'POST':
        update_comment = request.POST.get('update_comment')
        id = request.POST.get('commentId')
        dateTime=timezone.localtime(timezone.now())
        # print(id)
        # print(update_comment)
        Comment.objects.filter(comment_id=id).update(comment=update_comment,date_time=dateTime)
        return redirect('view_articles')
    return redirect('view_articles')

@csrf_exempt
def del_comment(request):
    if request.method == 'POST':
        commentID = request.POST['comment_id']    
        # print(commentID)
        Comment.objects.filter(comment_id=commentID).delete()
        return JsonResponse({'success': 'Comment Deleted Successfully'}) 
    return redirect('view_articles')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            uploaded_image = request.FILES['image']
            image_obj = ImageUpload.objects.create(image=uploaded_image)
            image_url = image_obj.image.url
            return JsonResponse({'image_url': image_url})
    else:
        return JsonResponse({'error': 'No image found or invalid request.'}, status=400)

@csrf_exempt
def delete_image(request):
    if request.method == 'POST':
        src_data = request.POST.get('img_src')
        add = src_data.replace('/','\\')
        print(add)
        absolutePath = str(os.getcwd())+add 
        if os.path.exists(absolutePath):
            os.remove(absolutePath)
        imgSource = src_data[7:]
        ImageUpload.objects.filter(image=imgSource).delete()
        return JsonResponse({'success':'image Deleted'})


def searchimage(directory):
    for filename in os.listdir(directory):
        pass