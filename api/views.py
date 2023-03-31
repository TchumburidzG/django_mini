from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from my_app.models import Projectebi, Review
from datetime import datetime



@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)
# ამ ზედა ფუნციით ვეუბნებით ჯანგოს თუ რომელ როუტებზე უნდა დააბრუნოს პასუხი.
# @api_view(['GET'])  გვჭირდება როცა გვაქ method based view. class based view-სთვის
# სხვა დეკორატორი გვჭირდება.
# '/api/projects/id' ამ როუტებს ვწერთ მერე urls.py-ში და შებამისად ვაბრუნებთ jsonresponce-ს.

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getProjects(request):
    print('User:', request.user)
    projects = Projectebi.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getProject(request, pk):
    project = Projectebi.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False).data
    return Response(serializer)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Projectebi.objects.get(id=pk)
    user = request.user.profile
    # იუზერი = რექვესტის_გამნახორციელებელი . იუზერის . პროფილს
    data = request.data
    # დეითა = რექვესტის . დეითას
    review, created = Review.objects.get_or_create(
        owner=user,
        projecti=project,
    )
    # აქ ამ created-ის ფუნქციაა ამ get_or_create-ის საშუალებიტ ასეთი რამე ნახავს თუ არის რივიუ
    # და თუ არ არის შექმნის. აქ  owner=user,  projecti=project  ეს  owner და projecti არიან
    # Review მოდელის ფილდები და იღებენ ჩვნე რიქვესტის მნიშვნელობებს.
    review.value = data['value']
    review.save()
    # ხმის მიცემა და შენახვა
    project.get_vote_count
    # აქ ვიძახებთ get_vote_count-ის ფუქქციას რო დაითვალოს პროცენტობა პოზიტიური და ნეგატიური შეფასებების პროცენტები
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)
# ამ ფუნქციის საშუალებით შეუძლია აუთენთიფიცირებულ იუზერს ხმა მიცეს პროექტს api-ის საშუალებით.