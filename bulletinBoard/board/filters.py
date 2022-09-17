from django_filters import FilterSet, ModelChoiceFilter

from .models import DeclarationResponse, Declaration


class ResponseFilter(FilterSet):
    declaration = ModelChoiceFilter(
        field_name='declaration',
        queryset=Declaration.objects.all()
    )
    class Model:
        model = DeclarationResponse

