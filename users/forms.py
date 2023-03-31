from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message




# UserCreationForm  რომ ჩავსვით როგორც პარამეტრი CustomUserCreationForm-ში ეს იმას ნიშნავს რომ
# CustomUserCreationForm გახდა ჩვეულებრივად ის რაც UserCreationForm იყო თავის ინფუთებით.
# views.py-ში რომ გვაქ ფუნქცია registerUser,  მანდ გვჭირდებოდა ეს UserCreationForm და ახლა შეგვიძლია
# იქ ამის მაგივრად უბრალოდ ეს ჩვენი ახლად შექმნილი კლასი class CustomUserCreationForm დავაიმპორტოთ
# და იგივე საქმეს გაგვიკეთებს იმიტო რომ იგივე ფუნქციონალიტეტი აქვს.
# ეს 'password1' და 'password2' გვჭირდება იმისთვის რო შედარდნენ პაროლები.
# მთლიანად ეს ფუქნცია იმისთვის გვჭირდება რომ UserCreationForm-ს ქონდა მარტო სამი ფილდი:
# Username, password და confirm password. ჩვენ კიდე ამით  ვამატებთ კიდევ ორს first_name-ს და  'email-ს
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }
        # ეს labels დიქშიონარი რეგისტრაციის გვერდზე First Names-ის მაგივრად ლეიბლს დაარქმევს Name.

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    # ეს ბოლო ფუქცია აკეთებს ასეთ რამეს რო ამ ფორმის ფილდები ამის გარეშე იყვნენ მოკლე და ვიწრო,
    # ამით კიდე კარგად გამოიყურებიან და ავსებენ სივრცეს



class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name',
            'username',
            'email',
            'location',
            'short_intro',
            'bio',
            'social_media',
            'wiki',
            'profile_pic']
        # ეს ლისტი იმიტო არის პროფილის მოდელის ლისტიდან ამოწერილი ფილდები რომლებიც გვინდა რომ იუზერმა
        # პროფილის რედაქტირებისას შეავსოს. შეგვეძლო გვქონდა '__all__' რაც ყველა ფილსდ გამოიტანადა.
        # ისეთებსაც რომლებიც საჭირო არაა.
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class UpdateSkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(UpdateSkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class WriteMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body', 'file']

    def __init__(self, *args, **kwargs):
        super(WriteMessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

