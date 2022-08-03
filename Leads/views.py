import logging
from django.contrib import messages
from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse, JsonResponse
from .models import Lead, Agent, Category, FollowUpModel
from .forms import LeadForm, LeadModelForm, CustomerCreationForm, AssignAgentForm, LeadCategoryUpdateForm, \
    CategoryModelForm, FollowupModelForm
from django.views.generic import TemplateView, ListView,DetailView, CreateView,UpdateView,DeleteView, FormView, View
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizerAndLoginRequiredMixin


logger = logging.getLogger(__name__)

class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomerCreationForm

    def get_success_url(self):
        return reverse("Leads:Login")

class LandingPageView(TemplateView):
    template_name = "landing.html"


class LeadListView(LoginRequiredMixin, ListView):
    template_name = "Leads/lead_list.html"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile,
                agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization,
                agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile,
                agent__isnull=True)
            context.update({
               "unassigned_leads" : queryset
            })
        return context

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "Leads/lead_detail.html"
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset

class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = "Leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("Leads:Lead")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.organization = self.request.user.userprofile
        form.save()

        send_mail(
            subject="A lead has been created successfully",
            message="Go to the site to see the new Lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )

        messages.success(self.request, "You have successfully created a lead")

        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = "Leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset


    def get_success_url(self):
        return reverse("Leads:Lead")

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "Leads/lead_delete.html"


    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse("Leads:Lead")

class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView):
    template_name = "Leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request" : self.request
        })
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(AssignAgentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("Leads:Lead")

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "Leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile
                )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization
                )


        context.update({
            "Unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
                )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
                )

        return queryset

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "Leads/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

      # qs = Lead.objects.filter(category=self.get_object())  u can use this or

        leads = self.get_object().leads.all()

        context.update({
            "leads":leads
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
                )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
                )
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "Leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization
            )

            # filters for logged in agent
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("Leads:Lead_detail", kwargs={"pk" : self.get_object().id})

class FollowupCreateView(LoginRequiredMixin, CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowupModelForm

    def get_success_url(self):
        return reverse("Leads:Lead_detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowupCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead" : Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowupCreateView, self).form_valid(form)

class CategoryCreateView(OrganizerAndLoginRequiredMixin,CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)

class FollowUpUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "Leads/followup_update.html"
    form_class = FollowupModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = FollowUpModel.objects.filter(
                lead__organization=user.userprofile
            )
        else:
            queryset = FollowUpModel.objects.filter(
                lead__organization=user.agent.organization
            )

            # filters for logged in agent
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("Leads:Lead_detail", kwargs={"pk" : self.get_object().lead.id})

class FollowUpDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "Leads/followup_delete.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = FollowUpModel.objects.filter(
                lead__organization=user.userprofile
            )
        else:
            queryset = FollowUpModel.objects.filter(
                lead__organization=user.agent.organization
            )

            # filters for logged in agent
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):

        followup = FollowUpModel.objects.get(pk=self.kwargs["pk"])
        return reverse("Leads:Lead_detail", kwargs={"pk": followup.lead.pk})

class LeadJsonView(View):
    def get(self, request, *args, **kwargs):

        qs = Lead.objects.all()

        return JsonResponse({
            "name": "test",
            "age": 33
        })


# def lead_update_view(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         print("receiving a request")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print("valid form")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#
#             return redirect("/Leads")
#
#     context = {
#         "lead":lead,
#         "form": form,
#     }
#     return render(request, "Leads/lead_update.html", context)


# def lead_create(request):
#     form = LeadForm()
#     if request.method == "POST":
#         print("receiving a request")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print("valid form")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name = last_name,
#                 age = age,
#                 agent = agent
#
#             )
#             return redirect("/Leads")
#     context = {
#         "form" : form
#     }
#     return render(request,"Leads/lead_create.html", context)


def landing_page(request):
    return render(request, "landing.html")

def Lead_list(request):
    leads = Lead.objects.all()
    context ={
        "object_list" : leads
    }

    return render(request,"Leads/lead_list.html", context)

def Lead_detail(request, pk):

    lead = Lead.objects.get(id=pk)
    context ={
        "lead": lead
    }
    return render(request, "Leads/lead_detail.html", context)

def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        print("receiving a request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            # print("valid form")
            # print(form.cleaned_data)
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # age = form.cleaned_data['age']
            # agent = form.cleaned_data['agent']
            # Lead.objects.create(
            #     first_name=first_name,
            #     last_name = last_name,
            #     age = age,
            #     agent = agent
            #
            # )

            form.save()
            return redirect("/Leads")
    context = {
        "form" : form
    }
    return render(request,"Leads/lead_create.html", context)

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method=="POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/Leads")

    context = {
        "form": form,
        "lead" : lead
    }
    return render(request, "Leads/lead_update.html", context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/Leads")