from .models import Profile, Skill
from django.db.models import Q    # Q ნიშნავს სავარაუდოდ ქვერის. და გვჭრდება ქვემოტ სირჩისთვის
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger



def search_profiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)
    # შეგვეძლო ასეც დაგვეწერა skills = Skill.objects.filter(name__exact=search_query)
    # მარა ეს მოძებნის მარტო ზუსტ დამთხვევებს
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills))
    # ეს ზედა ხაზი ამ name__icontains-ის საშუალებით მოძებნის პროფილების ცხრილში იმ სახელებს,
    # რომლებიც შეიცავენ search-ში ჩაწერილ ტექსტს. ერთ ასოს ან ასოების თანმიმდევროვრობას ეძებს.
    # | ეს არის or და ეს &  and ოპერატორი და გვაქ კიდე ეს Q რომლითაც მოვძებნით თუ სადმე სახელში ან შორთ ინტროში სადმე
    # ჩვენი საძიებო ტექსტია. Q უნდა დავაიმპორტოთ ჯერ აქედან from django.db.models import Q  და მერე გამოვიყენებთ
    # ორი ან მეტი სხვადასხვა ქვერების ერთდროულად გამოსაყენებლად.
    # ამ distinct()-ის გარეშე გამოტანს ერთიდაიგივე პროფილს იმდენჯერ რამდენჯერაც ჩვენი საძიებო სიტყვა ამ ქვერებიდან
    # ერთს ან რამდენიმეს ერთად დაემთხვევა. ამით კიდე თითოეულ მოძიებულ პროფილს მარტო ერთხელ.


    # ქვემოთ როა search_query. მაგას გავიტანთ HTML-ში სადაც სირჩის იფუთია აი ასე value="{{ search_query }}
    # და ერხელ როჩავწერთ სირჩში რამეს იმას აღარ წაშლის და placeholder-ს არ გამოაჩენს არამედ დატოვებს ბოლოს ჩაწერილ ტექსტს
    # რომელიც შემდეგ შეგვიძლია დავარედაქტიროთ და ა.შ.

    return profiles, search_query


def paginate_profiles(request, profiles, results):
    page = request.GET.get('page')

    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles