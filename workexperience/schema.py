import graphene
from graphene_django import DjangoObjectType
from .models import WorkExperience
from users.schema import UserType
from django.db.models import Q

class WorkExperienceType(DjangoObjectType):
    class Meta:
        model = WorkExperience

class Query(graphene.ObjectType):
    positions = graphene.List(WorkExperienceType, search=graphene.String())
    positionById = graphene.Field(WorkExperienceType, idWorkExperience=graphene.Int())

    def resolve_positions(self, info, search=None, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print (user)
        if (search=="*"):
            filter = (
                Q(posted_by=user)
            )
            return WorkExperience.objects.filter(filter)[:10]
        else:
            filter = (
                Q(posted_by=user) & Q(position__icontains=search)
            )
            return WorkExperience.objects.filter(filter)
        
    def resolve_positionById(self, info, idWorkExperience, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print (user)

        filter = (
            Q(posted_by=user) & Q(id = idWorkExperience)
        )
        return WorkExperience.objects.filter(filter).first()
        
class CreateWorkExperience(graphene.Mutation):
    idWorkExperience   = graphene.Int()
    position     = graphene.String()
    company = graphene.String()
    location = graphene.String()
    description = graphene.String()
    start_date = graphene.Date()
    end_date   = graphene.Date()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        idWorkExperience= graphene.Int()  
        position     = graphene.String()
        company = graphene.String()
        location = graphene.String()
        description = graphene.String()
        start_date = graphene.Date()
        end_date   = graphene.Date()

    #3
    def mutate(self, info, idWorkExperience, position, company,  location, description , start_date, end_date):
        user = info.context.user or None
        if user.is_anonymous:
            raise Exception('Not logged in !');
        print(user)

        currentWorkExperience = WorkExperience.objects.filter(id=idWorkExperience).first()
        print (currentWorkExperience)

        workExperience = WorkExperience(
            position = position,
            location = location,
            description = description,
            start_date = start_date,
            end_date   = end_date,
            posted_by  = user
            )
        
        if currentWorkExperience:
            workExperience.id = currentWorkExperience.id

        workExperience.save()

        return CreateWorkExperience(
            idWorkExperience  = workExperience.id,
            position = workExperience.position,
            location = workExperience.location,
            description = workExperience.description,
            start_date = workExperience.start_date,
            end_date   = workExperience.end_date,
            posted_by  = workExperience.posted_by
        )

class DeleteWorkExperience(graphene.Mutation):
    idWorkExperience=graphene.Int()

    #2 
    class Arguments: 
        idWorkExperience= graphene.Int()

    #3
    def mutate(self, info, idWorkExperience):
        user = info.context.user or None

        if user.is_anonymous:
            raise Exception('Not logged in!')
        print (user)

        currentWorkExperience = WorkExperience.objects.filter(id=idWorkExperience).first()
        print (currentWorkExperience)

        if not currentWorkExperience:
            raise Exception('Invalid WorkExperience id')
        
        currentWorkExperience.delete()

        return DeleteWorkExperience(
            idWorkExperience = idWorkExperience,
        )
        
#4
class Mutation(graphene.ObjectType):
    create_workExperience = CreateWorkExperience.Field()
    delete_workExperience = DeleteWorkExperience.Field()

