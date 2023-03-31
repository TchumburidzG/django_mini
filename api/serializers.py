from rest_framework import serializers
from my_app.models import Projectebi, Review, Tag
from users.models import Profile, Skill


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    # ამ ზედა ხაზი აკეთებს ასეთ რამეს: პროქტების მოდელებში სადაც owner ფილდია იქ
    # უბრალოდ აიდის მაგივრად გამოიტანს მთლიანად ამ owner-ის პროფილის მოდელებს.
    # რათქმაუნდა ჯეისონ ფორმატში და ჩაშლილი იქნება მონაცემები.
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    # პროექტების მოდელებს რახან reviews-ს ფილდი არ აქვს ვერ გამოვა ამ პროქტის reviews-ის
    # ასე მარტივად გამიტანა, როგორც ეს ზემოთ owner-ის შემთხვევაში იყო.
    # ამჯერად გვჭირდება ფუნქცია-მეთოდი get_reviews, სადაც აქ get_reviews(self, obj)
    # ეს obj  არის Projectebi-ის მოდელი საიდანაც review_set.all()-ის საშალებით
    # ვიღებთ ყველა რივიუს რომელიც ამ შესაბამის პროექტთან ასოცირდება.
    # serializer = ReviewSerializer(reviews, many=True) აქ კიდე უბრალოდ სერიალაიზერს
    # არგუმენტად ვაძლევთ ამ ჩვენ reviews-ებს.
    # ეს .data  შეგვიძლია return-ისასაც მივაწეროთ და მანამდეც მაგ. ასე:
    # serializer = ReviewSerializer(reviews, many=True).data
    class Meta:
        model = Projectebi
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


