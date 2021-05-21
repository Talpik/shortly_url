import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import URL


class URLType(DjangoObjectType):
    """
    Создаём новый тип GraphQL для модели URL
    """
    class Meta:
        model = URL


class Query(graphene.ObjectType):
    urls = graphene.List(URLType, url=graphene.String(), first=graphene.Int(), skip=graphene.Int())

    def resolve_urls(self, info, url=None, first=None, skip=None, **kwargs):
        queryset = URL.objects.all()

        if url:
            _filter = Q(full_url__icontains=url)
            queryset = queryset.filter(_filter)

        if first:
            queryset = queryset[:first]

        if skip:
            queryset = queryset[skip:]

        return queryset


class CreateURL(graphene.Mutation):
    """
    url - определяет содержание, возвращаемое сервером после завершения мутации.
    В этом случае это структура данных с типом URLType.
    """
    url = graphene.Field(URLType)

    class Arguments:
        full_url = graphene.String()

    def mutate(self, info, full_url):
        url = URL(full_url=full_url)
        url.save()


class Mutation(graphene.ObjectType):
    """
    Класс Mutation для хранения всех мутаций приложения
    """
    create_url = CreateURL.Field()
