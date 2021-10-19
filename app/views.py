from typing import Optional

from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from app import forms
from app.models import Review
from app.models import Ticket
from app.models import UserFollows


# Create your views here.
@login_required(login_url='login')
def index_view(request):
    context = {}
    return render(request, 'index.html', context)


@login_required(login_url='login')
def feed_view(request):
    followed_users = list(UserFollows.objects.filter(user_id=request.user.id))
    followed_users__ids = [
        followed_user.followed_user_id for followed_user in followed_users
    ]
    feed_ids = followed_users__ids + [request.user.id]
    tickets = list(Ticket.objects.filter(user_id__in=feed_ids))
    reviews = list(Review.objects.filter(user_id__in=feed_ids))
    user_reviews = list(Review.objects.filter(user_id=request.user.id))
    user_reviews__ticket_ids = [
        user_review.ticket_id for user_review in user_reviews
    ]
    tickets_and_reviews = sorted(
        tickets + reviews,
        key=lambda item: item.time_created,
        reverse=True
    )
    context = {
        "tickets_and_reviews": tickets_and_reviews,
        "user_reviews__ticket_ids": user_reviews__ticket_ids
    }
    return render(request, 'feed.html', context)


@login_required(login_url='login')
def posts_view(request):
    tickets = list(Ticket.objects.filter(user=request.user))
    reviews = list(Review.objects.filter(user=request.user))
    tickets_and_reviews = sorted(
        tickets + reviews,
        key=lambda item: item.time_created,
        reverse=True
    )
    context = {"tickets_and_reviews": tickets_and_reviews}
    return render(request, 'posts.html', context)


@login_required(login_url='login')
def account_follow_view(request):
    context = {}
    user = get_user_model()
    followed_users = list(user.objects.filter(
        followed_by__in=UserFollows.objects.filter(
            user_id=request.user.id
        )
    ))
    url_parameter = request.GET.get("q")

    if url_parameter:
        users = user.objects.filter(
            username__icontains=url_parameter
        ).exclude(id=request.user.id)
    else:
        users = user.objects.all().exclude(id=request.user.id)

    context["users"] = users
    # context["serzd_users"] = serializer.serialize("json", users)
    context["followed_users"] = followed_users

    if request.is_ajax():
        html = render_to_string(
            template_name="user_results_partial.html",
            context={
                "users": users,
                "followed_users": followed_users
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "account_follow.html", context=context)


@login_required(login_url='login')
@csrf_exempt
def follow(request, user_id):
    users_to_follow = get_user_model()
    UserFollows(
        user=request.user,
        followed_user=users_to_follow.objects.get(pk=user_id)
    ).save()

    return account_follow_view(request)


@login_required(login_url='login')
@csrf_exempt
def unfollow(request, user_id):
    UserFollows.objects.get(followed_user_id=user_id).delete()

    return account_follow_view(request)


class NewReviewRequest(LoginRequiredMixin, CreateView):
    """
    review request <==> ticket
    """

    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.NewReviewRequestForm
    success_url = reverse_lazy('feed')
    template_name = 'new_review_request.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.success_url)


class UpdateReviewRequest(LoginRequiredMixin, UpdateView):

    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.NewReviewRequestForm
    success_url = reverse_lazy('posts')
    template_name = 'edit_review_request.html'
    model = Ticket

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.success_url)


class DeleteReviewRequest(LoginRequiredMixin, DeleteView):

    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('posts')
    model = Ticket

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class NewReviewWithoutTicket(TemplateView):

    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    new_review_request_form = forms.NewReviewRequestForm
    new_review_form = forms.NewReviewForm
    success_url = reverse_lazy('feed')
    template_name = 'new_review_without_ticket.html'

    def post(self, request):
        post_data = request.POST or None
        post_files = request.FILES or None
        new_review_request_form = self.new_review_request_form(
            post_data, post_files, prefix="newreviewrequest"
        )
        new_review_form = self.new_review_form(
            post_data, prefix="newreview"
        )

        context = self.get_context_data(
            new_review_request_form=new_review_request_form,
            new_review_form=new_review_form
        )

        if new_review_request_form.is_valid() and new_review_form.is_valid():
            review_request = self.form_save(new_review_request_form)
            self.form_save(new_review_form, review_request)
            return HttpResponseRedirect(self.success_url)

        return self.render_to_response(context)

    def form_save(self, form, review_request=None) -> Optional[Ticket]:
        """
        This function returns a ticket (review_request) when it's
        called to save a ticket.
        This allows the form to be aware of it.
        Then, when the function is called to save a review, it sets the
        review's ticket member so that the "ticket_id" review foreign key
        field can be assigned later on by the model's constructor.
        """
        form.instance.user = self.request.user
        if review_request:
            review = form.save(commit=False)
            review.ticket = review_request
            review.save()
            return
        review_request = form.save()
        return review_request

    def get(self, request, *args, **kwargs):
        return self.post(request)


class NewReviewWithTicket(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.NewReviewForm
    success_url = reverse_lazy('feed')
    template_name = 'new_review_with_ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = Ticket.objects.get(
            pk=self.kwargs["ticket_id"]
        )
        print(context["ticket"].image.url)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        review = form.save(commit=False)
        context = self.get_context_data()
        review.ticket = context["ticket"]
        review.save()
        return super().form_valid(form)


class UpdateReview(LoginRequiredMixin, UpdateView):

    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.NewReviewForm
    success_url = reverse_lazy('posts')
    template_name = 'edit_review.html'
    model = Review

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class DeleteReview(LoginRequiredMixin, DeleteView):

    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('posts')
    model = Review

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SignUp(CreateView):

    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        self.request.session['email'] = self.request.POST.get('email')
        form.save()
        return super().form_valid(form)


class Login(LoginView):

    form_class = forms.UserLoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'
    fields = '__all__'


class Logout(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(Logout, self).get_redirect_url(*args, **kwargs)
