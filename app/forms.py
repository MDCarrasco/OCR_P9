from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import HiddenInput
from django.forms import ModelForm
from django.forms import IntegerField
from django_starfield import Stars

from app.models import Ticket
from app.models import Review


class NewReviewForm(ModelForm):
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    """

    class Meta:
        fields = ('headline', 'rating', 'body')
        model = Review

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['headline'].label = 'Titre'
        self.fields['headline'].required = True
        self.fields['rating'] = IntegerField(widget=Stars)
        self.fields['rating'].label = 'Note'
        self.fields['rating'].required = True
        self.fields['body'].label = 'Description'
        self.fields['body'].required = True


class NewReviewRequestForm(ModelForm):
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    """

    class Meta:
        fields = ('title', 'description', 'image')
        model = Ticket

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Titre'
        self.fields['title'].required = True
        self.fields['description'].required = True


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Adresse e-mail"
        self.fields['email'].required = True

    '''
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Cet e-mail est déjà utilisé par un autre utilisateur.")
        return self.cleaned_data['email']
    '''


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur (pseudonyme)"
