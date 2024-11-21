import graphene
from graphene_django import DjangoObjectType
from .models import Header
from users.schema import UserType
from django.db.models import Q

class HeaderType(DjangoObjectType):
    class Meta:
        model = Header

class Query(graphene.ObjectType):
    headers = graphene.List(HeaderType, search=graphene.String())
    headerById = graphene.Field(HeaderType, idHeader=graphene.Int())

    def resolve_headers(self, info, search=None, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print (user)
        if (search=="*"):
            filter = (
                Q(posted_by=user)
            )
            return Header.objects.filter(filter)[:10]
        else:
            filter = (
                Q(posted_by=user) & Q(title__icontains=search)
            )
            return Header.objects.filter(filter)
        
    def resolve_headerById(self, info, idHeader, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print (user)

        filter = (
            Q(posted_by=user) & Q(id = idHeader)
        )
        return Header.objects.filter(filter).first()
        
class CreateHeader(graphene.Mutation):
    idHeader   = graphene.Int()
    title     = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        idHeader= graphene.Int()  
        title     = graphene.String()
        description = graphene.String()


    #3
    def mutate(self, info, idHeader, title, description):
        user = info.context.user or None
        if user.is_anonymous:
            raise Exception('Not logged in !');
        print(user)

        currentHeader = Header.objects.filter(id=idHeader).first()
        print (currentHeader)

        headers = Header(
            title = title,
            description = description,
            posted_by  = user
            )
        
        if currentHeader:
            headers.id = currentHeader.id

        headers.save()

        return CreateHeader(
            idHeader  = headers.id,
            title    = headers.title,
            description = headers.description,
            posted_by  = headers.posted_by
        )

class DeleteHeader(graphene.Mutation):
    idHeader=graphene.Int()

    #2 
    class Arguments: 
        idHeader= graphene.Int()

    #3
    def mutate(self, info, idHeader):
        user = info.context.user or None

        if user.is_anonymous:
            raise Exception('Not logged in!')
        print (user)

        currentHeader = Header.objects.filter(id=idHeader).first()
        print (currentHeader)

        if not currentHeader:
            raise Exception('Invalid Header id')
        
        currentHeader.delete()

        return DeleteHeader(
            idHeader = idHeader,
        )
        
#4
class Mutation(graphene.ObjectType):
    create_Header = CreateHeader.Field()
    delete_Header = DeleteHeader.Field()
