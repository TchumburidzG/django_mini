from django.db import models
import uuid
from users.models import Profile

# Create your models here.


class Projectebi(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=200, null=True, blank=True)
    source_link = models.CharField(max_length=200, null=True, blank=True)

    #ესენი ჩვეულებრივი ფილდებია
    # null=True, არის რომ მონაცემთა ბაზა დათანხმდეს ცარიელ ფილდს და blank=True არის რო ჯანგო დათანხმდეს
    featured_image = models.ImageField(null=True, blank=True, default='default_img.png')
    # python -m pip install pillow ეს ბრძანება უნდა გავუშვათ ტერმინალში აი ამან default='default_img.png'  რო იმუშაოს.
    # მარა მარტო ეგ არ ყოფნის, პითონის  ბიბლიოთეკაა საჭირო. ინსტალაცია: python -m pip install whitenoise და
    # settings.py-ში, MIDDLEWARE -ში ამ ჩანაწერის დამატება "whitenoise.middleware.WhiteNoiseMiddleware"
    # ამ დროს ყველაფრის ჩვენება ხდება staticfiles-დან და არა static-დან იმიტომ რომ DEBUG = False,
    # რაც იმას ნიშნავს რომ თუ რამე ცვლილებას
    # შევიტანთ სადმე სტატიკურ ფაილებში (css, html, ფოტო და ა.შ) ბრაუზერში ვერ დავინახავთ, ანუ არ შეიცვლება.
    # საჭიროა გავუშვათ ბრძანება python manage.py collectstatic ან DEBUG = True-ზე დავაყენოთ

    created = models.DateTimeField(auto_now_add=True)

    # ამ სამ შორის ჯერ არ ვიცი განსხვავება მარა ეს მესამე საათის და თარიღის ჩასაწერს აგდებს და უნდა ჩავწეროთ ან ავირჩიოთ

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    # UUIDField არის 16 ნიშნა აიდი ციფრებითა და ასოებით.
    # default=uuid.uuid4 ეს არის დაშიფვრის მეთოდი
    # unique=True ამას ვწერთ თუ გვინდა რომ აიდი უნიკალური იყოს
    # primary_key=True ამას ვწერთ თუ გვინდა რომ აიდი primary key-დ გამოვიყენოთ.
    # editable=False დაედითება აკრძალულია

    tags = models.ManyToManyField('Tag', blank=True)
    #ამ ხაზით ვუკავშირებთ ერთმანეთს ამ და ქვემოთ დაწერილ ცვრილს (Tag). 'Tag' იმიტოა ბრჭყალებშ რომ მაგის კლასის ქვემოთაა,
    #ამ კლასის ზემოთ რო წერებულიყო ბრჭყალების გარეშეც წავა.
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # ზედა დათვლის მიცემულ ხმებს ქვედა პროცენტებს


    def __str__(self):
        return self.title   # აქ რასაც დავწერთ ამას დაარქმევს ადმინის ექაუნთში ჩვენ პროექტებს



    """
    class Meta:
        ordering = ['created']
    
        # ეს დაალაგებს პროექტებს შექმნის თარიღის მიხედვით. თუ დავწერდით  '-created' მაშინ შებრუნებულად მარა ისევ თარიღით
        # 'created'-ის მაგივრად შევიძლია ასევე სხვა პარამეტრის არჩვეაც...
    """


    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']
        # ეს დაალაგებს პროექტებს -vote_ratio-ს მიხედვით. თუ -vote_ratio ტოლები აქ ორს მაშინ  'vote_total'-ის
        # მიხედვით და თუ ეგეც ტოლებია მაშინ 'title'-ის მიხედვით. ზედა მეტა აღარ გვჭირდება.
        # ანუ das heißt შეგვიძლია პროექტები ან სხვა რამეებიც ყოველტვის დავალაგოთ მოდელში არსებული
        # რომელიმე ფილდის ან ფილდების  მიხედვით

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
        # გადმოიტანს ყველა რივიუს "review_set.all()" ვალუების
        # (value არის ტექსტის ფილდი რივიუს მოდელებში) "values_list"
        # ოუნერებს (ანუ ვინც დაწერა)  ლისტის სახით "owner__id".
        # ეს flat=True რას აკეთებს კარგად ვერ გავიგე

    @property    # ამ @property-ს ტუ დავაკომენტარებს get_vote_count ყვითლად არარ იქნება. საინტერესოა....
    def get_vote_count(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()
    # ეს ფუქცია თვლის პროექტების რივიუებს და პოზიტიური რივიუების პროცენტობას. მე მგონი ყველაფერი გასაგებია

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up vote'),
        ('down', 'Down vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    # ამ ზედა ხაზით ვაბამთ პროფილს ForeignKey-ით კომენტარის ავტორზე.
    # ანუ ავტომატურად კომენტარის ავტორი იქნება ის ვისი ფროფილიდანაც დაიწერა.
    projecti = models.ForeignKey(Projectebi, on_delete=models.CASCADE)
    #  on_delete=models.SET_NULL ან CASCADE . განსხვავება არის რომ მშობელი ცხრილის წაშლისას პირველ შემთხვევაში
    # შვილი ცხრილები დარჩებიან მეორე შეთხვევაში კი ესეც ავტომატურად წიშლება.
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=20, choices=VOTE_TYPE)
    # choices=VOTE_TYPE  ამით შექმნება ამოსარჩევი პასუხები ანუ ჩამონათვალი უნდა ავირჩიოთ

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'projecti']]
        # ამ მეტა კლასით, სადა unique_together უდრის ცხრილს ცხრილში 'owner' და  'projecti'
        # რომლებიც ამავე მოდელში გვაქ ვაკეთებთ (ვეუბნებით ჯანგოს) ასეთ რამეს რომ ეს ორი 'owner' და  'projecti'
        # ერთად უნიკალურები არიან და 'owner'-ს არ შეუძლია საკუტარ თავს კომენტარი დაუწეროს.


    def __str__(self):
        return self.value




class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return self.name
    # ამ თაგებით შეგვიძლია დავთაგოთ პროექტები და პროქტს რო გავხსნიტ გამოჩნდებიან რითიც დავთაგავთ
























