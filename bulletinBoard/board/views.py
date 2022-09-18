from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User, Permission, AnonymousUser
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)

from allauth.account.views import SignupView

from .forms import ActivationForm, DeclarationForm, DeclarationResponseForm
from .models import UserActivation, Declaration, DeclarationResponse
from .filters import ResponseFilter


class CustomSignupView(SignupView):
    def form_valid(self, form):
        super().form_valid(self, form)
        return HttpResponseRedirect('/account/activate/')

@login_required
def user_activation_view(request):
    user = request.user
    context = {}
    if not UserActivation.objects.get(user=user).user_activated:
        if request.POST:
            key = request.POST['activation_code']
            check_table = UserActivation.objects.get(user=user)
            if check_table.user == user and check_table.secret_key == key:
                check_table.user_activated = True
                check_table.save()
                user_perm = User.objects.get(email=request.user.email).user_permissions.add(Permission.objects.get(codename='add_declaration'), Permission.objects.get(codename='add_declarationresponse'))

                return HttpResponseRedirect('/')
            else:
                context['activate_error_incorrect_code'] = False
                return render(request=request, template_name='activation.html', context=context)
        else:
            context['form'] = ActivationForm()
        return render(request=request, template_name='activation.html', context=context)
    else:
        context['is_activate'] = True
        return HttpResponseRedirect('/')


class BoardView(ListView):
    model = Declaration
    ordering = '-date'
    template_name = 'declarations.html'
    context_object_name = 'declarations'


class DeclarationView(DetailView):
    model = Declaration
    template_name = 'declaration.html'
    context_object_name = 'declaration'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == context['declaration'].author:
            context['responses'] = DeclarationResponse.objects.filter(declaration=context['declaration'])
        elif self.request.user in UserActivation.objects.filter(user_activated=True):
            context['responses'] = DeclarationResponse.objects.filter(author=self.request.user)
        return context


class ResponseView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('board_adddeclaration', )
    model = DeclarationResponse
    template_name = 'response.html'
    context_object_name = 'response'


class UserResponsesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('board.add_declaration')
    model = DeclarationResponse
    ordering = '-date'
    template_name = 'user_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        return context


class DeclarationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_declaration', )
    model = Declaration
    form_class = DeclarationForm
    template_name = 'create.html'

    def form_valid(self, form):
        declaration = form.save(commit=False)
        declaration.author = self.request.user
        declaration.save()
        return HttpResponseRedirect(f'/declaration/{declaration.pk}')


class DeclarationResponseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_declarationresponse', )
    model = DeclarationResponse
    form_class = DeclarationResponseForm
    template_name = 'create.html'

    def form_valid(self, form):
        declaration_response = form.save(commit=False)
        declaration_response.author = self.request.user
        declaration_pk = self.request.META['PATH_INFO'].split('/')[2]
        declaration_response.declaration = Declaration.objects.get(pk=int(declaration_pk))
        declaration_response.save()
        return HttpResponseRedirect(f'/declaration/{declaration_pk}/')


class DeclarationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('board.add_declaration', )
    model = Declaration
    template_name = 'delete.html'
    success_url = reverse_lazy('declarations')

class DeclarationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('board.add_declaration', )
    model = Declaration
    form_class = DeclarationForm
    template_name = 'edit.html'

    def form_valid(self, form):
        declaration = form.save(commit=False)
        if declaration.author != self.request.user:
            return HttpResponseForbidden('NO-NO-NO! Its not your', status=403)
        declaration.save()
        return HttpResponseRedirect(f'/declaration/{declaration.pk}/')


@login_required
def delete_response(request, pk):
    response = DeclarationResponse.objects.get(pk=pk)
    if response.declaration.author == request.user:
        DeclarationResponse.objects.get(pk=pk).delete()
        return HttpResponseRedirect('/userresponses/')
    return HttpResponseRedirect('/userresponses/')


@login_required
def accepte_response(request, pk):
    response = DeclarationResponse.objects.get(pk=pk)
    if response.declaration.author == request.user:
        response.accepted = True
        response.save()
        return HttpResponseRedirect('/userresponses/')
    return HttpResponseRedirect('/userresponses/')