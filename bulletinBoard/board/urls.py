from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (user_activation_view,
                    BoardView,
                    DeclarationView,
                    ResponseView,
                    DeclarationCreateView,
                    DeclarationResponseCreateView,
                    UserResponsesView,
                    DeclarationUpdateView,
                    delete_response,
                    accepte_response,
                    DeclarationDeleteView
                    )

urlpatterns = [
    path('account/activate/', user_activation_view, name='activation'),
    path('', BoardView.as_view(), name='declarations'),
    path('declaration/<int:pk>/', DeclarationView.as_view()),
    path('declaration/<int:pk>/delete', DeclarationDeleteView.as_view()),
    path('declaration/create/', DeclarationCreateView.as_view()),
    path('response/<int:pk>/', ResponseView.as_view()),
    path('response/<int:pk>/delete/', ResponseView.as_view()),
    path('response/<int:pk>/accept', accepte_response),
    path('response/<int:pk>/delete', delete_response),
    path('declaration/<int:pk>/createresponse/', DeclarationResponseCreateView.as_view()),
    path('userresponses/', UserResponsesView.as_view()),
    path('declaration/<int:pk>/edit/', DeclarationUpdateView.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)