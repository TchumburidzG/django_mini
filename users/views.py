from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, UpdateSkillForm, WriteMessageForm
from .models import Profile, Skill, Message
from django.contrib.auth.decorators import login_required
from .utils import search_profiles, paginate_profiles
from django.core.files.storage import FileSystemStorage

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    # ეს ზედა ორი ხაზი აკეთებს ასეთ რამეს:
    # თუ შესული ვართ ექაუნთზე და ბრაუზერის საძებნელ ველში ჩავწერთ ხელით login არ გადავა login-ის გვერდზე,
    # არამედ დაგვაბრუნებს უკან profiles-ების გვერდზე
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, " Username doesn't exist ")
            #  ეს ზედა ერთი ხაზი აკეთებს HTML-თან ერთდად ასეთ რამმეს:
            #  თუ იუზერი შეცდომით ჩაწერს სახელს ან პაროლს ეს გამოუტანს ტექტს რომ
            #  მომხმარებლის სახელი ან პაროლი შეცდომითაა ჩაწერილი
            # ქვემოტაც არის რამდენიმე ასეთი

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
            # თუ გვაქ 'next' მისამართი მაშინ redirect next-ზე თუ არა მაშინ account-ზე.
            # ეს იმისთვის გვინდა, რომ, როცა იუზერი რამე ისეთ მოქმედებას აკეთებს (მაგ: კომენტარის დაწერა)
            # რომელისთვისაც შესული უნდა იყოს ექაუნთზე და ვამისამართებ შესვლის გვერდზე შესვლის
            # შემდეგ ავტომატურად ჩამოეტვირთოს ის გვერდი ისევ სადაც იყო.
            # (მაგ: იმ პროექტის გვერდი სადაც კომენტარს წერდა).
            # დამატებით Login_register.html-ში ლოგინის ფორმის action="" ცარიელი სტრინგი უნდა
            # იყოს და არა action="{.% url 'login' %}" ეს რომ გამოვიდეს
        else:
            messages.error(request, ' username or password is incorrect')

    return render(request, 'users/login_register.html')



def logoutUser(request):
    logout(request)
    messages.info(request, " You are now logged out ")
    # აქ ზემოთ რო messages.info წერია და სხვაგან messages.error მაგით შეგვიძლია მოგვიანებით html-ში ერორ მესიჯების
    # ფერები ვცვალოთ. ანუ ლურჯი: დაინფორმაციო და წითელი: ერორი
    return redirect('login')
    # ეს ხაზი  return redirect('login') გამოსვლისას ავტომატურად გადაგვივანს ('login') გვერდზე.
    # ანუჩამოტვირთავს იმას რაც url-ებში რაც 'login'-ის გვერდზეა გაწერილი



def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account') # რეგისტრაციის დასრულებისას გადაგვიყვანს ეს ავტომარურად edit-account-ის გვერდზე
        else:
            messages.success(request, 'An error has occurred during registration!')
    # ეს ზედა რამდენიმე ხაზი და if-ები აკეთებენ შემდეგ რამეს:
    # თუ request.method == 'POST': მაშინ შეინახე ეს ჩვენი ფორმები user-ში მარა არა ბაზაში (commit=False) არ დააკომიტო.
    # მერე იუზერნეიმში თუა დიდი ასოები დააპატარავე ყველა : user.username = user.username.lower()
    # და მერე შეინახე ასე დაპატარავებული user.save()
    # ეს ხაზი კიდე წარმატებული რეგისტრაციის შემთხვევაში გვეტყვის რომ
    # დავრეგისტრირდით messages.success(request, 'User account was created!').
    # ამ მთლიანი კოდის მაგივრად შეგვეძლო უფრო მოკლეც ჩაგვეწერა:
    #     if request.method == 'POST':
    #         form = UserCreationForm(request.POST)
    #         if form.is_valid():
    #             user.save()
    #             messages.success('User account was created!')
    # ასე მაგალითად მარა ამ შემთხვევაში შეიძლება მივიღოთ ასეთი სიტუაცია რომ დარეგისტრირდეს ორი იუზერი
    # ერთნაირი სახელებით Besika და besika. ქვედა if-ით  კიდე ამას ვარიდებთ თავს.

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = search_profiles(request)
    custom_range, profiles = paginate_profiles(request, profiles,6)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range }
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user_profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.projectebi_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects }
    return render(request, 'users/account.html', context)



@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    # ანუ რა ხდება აქ: ფორმა = იმ ფორმას forms.py-ში რო გვაქ. იქ კიდე მოდელებიდანგადმოვიტანეთ.
    # ანუ პირდაპირ მოდელიდან ვერ შევქმნით ტექსტბოქსებს და რაღაცეებს იუზერებმა რო შეძლონ შევსება.
    # models.py --> forms.py --> view.py.
    # instance=profile ეს რაღაცა კიდე ასეთ რამეს აკეთებს: უკვე არსებულ პროფილს რომ ვაედითებთ შესაბამისად აქვს იმას
    # ზოგიერთი ფილდი უკვე შევსეული და ეს ავტომატურად გამოიტას ედიტისას წინ
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)



@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':            # ეს ორ ხაზირ არის იმისტვის რომ შევსებული ფილდები დაიმახსოვროს
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            messages.success(request, 'Skill was added successfully')
            skill.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = UpdateSkillForm(instance=skill)
    if request.method == 'POST':            # ეს ორ ხაზი არის იმისთვის რომ შევსებული ფილდები დაიმახსოვროს
        form = UpdateSkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)



@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read=False).count()
    context = {'messageRequests': messageRequest, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)



@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)



@login_required(login_url='login')
def sendMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = WriteMessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = WriteMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'you message was successfully sent ')
            return redirect('profile', pk=recipient.id)
    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
