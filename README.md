# JApp

How I write Django apps.

JApp is a convention, that I use to write django apps. It's like a template to make writing Django apps easier and
faster. It comes with ready to use templates, mixins, styled forms and a lot more.

# Get Started

Start a project:

```shell
django-admin startproject mysite
cd mysite
```

Clone the repo using git:

```shell
git clone https://github.com/youzarsiph/JApp.git
```

Install JApp, in `mysite/settings.py`:

```python
INSTALLED_APPS = [
    'JApp.apps.JAppConfig',  # Add this line
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions'  # We need this to rename the app
]
```

Include `urls.py` from the JApp, in `mysite/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include  # import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('JApp.urls')),  # Add this line
]
```

Run migrate command:

```shell
python manage.py migrate
```

Run the server:

```shell
python manage.py runserver
```

Now enjoy!

# Tutorial: Create a blog

This tutorial assumes that you know the basics of Django, and it is a code based tutorial, so it is not widely
explained.

This tutorial starts where the Getting Started section ends. In this tutorial we are going to build a blog app using
JApp as a template.

We will start by renaming the JApp. To rename we need to install `django_extensions` to run the script:

```shell
pip install django_extensions
```

Rename JApp:

```shell
python manage.py runscript rename_app --script-args 'JApp' 'blog'
```

Change the dotted path of the JApp, in `mysite/settings.py`:

```python
INSTALLED_APPS = [
    # 'JApp.apps.JAppConfig',  # Change this line
    'blog.apps.BlogConfig',  # To this
    ...
]
```

Then change the include statement in `mysite/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('JApp.urls')),  # Change this line
    path('', include('blog.urls')),  # To this
]
```

## Models

Let's start with `blog/models.py`:

```python
from django.db import models
from django.conf import settings


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=128)
    image = models.ImageField(null=True, blank=True)
    about = models.CharField(max_length=512)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

```

This is the model that we will be working with.

## Views

In this section we are going to write our views. We are going to implement CRUD views.

### Create View

To style the form we need to create a class in `blog/forms/create.py`:

```python
from blog.forms.base import StyledModelForm
from blog.models import Post


class PostCreationForm(StyledModelForm):
    class Meta:
        model = Post
        fields = ('title', 'about', 'content', 'image')

```

Here is the code for `blog/views/create.py`:

````python
from blog.models import Post
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from blog.forms.create import StyledUserCreationForm, PostCreationForm
from blog.views.generic import CreationView, MessageRequiredCreationView
from blog.views.mixins import LoginRequiredMixin, UserRequiredMixin

...  # Keep as it is.


class PostCreationView(UserRequiredMixin, MessageRequiredCreationView):
    model = Post
    form_class = PostCreationForm
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Post created successfully.'
    error_message = 'An error occurred while processing.'

````

According to the convention, we need to create an HTML file with the name of the model. So we will create a file named
post.html in `blog/templates/blog/views/create/` folder. This convention applies to all views .

The code for `blog/templates/blog/views/create/post.html`:

```html
{% extends 'blog/views/create/template.html' %}
{% load i18n %}
{% block title %}{{ block.super }}{% translate 'Post' %}{% endblock %}
{% block page_title %}{% translate 'Create Post' %}{% endblock %}
```

### List & Detail Views

Here is the code for `blog/views/list.py`:

```python
from blog.models import Post
from blog.views.generic import ListingView


class PostListView(ListingView):
    model = Post
    paginate_by = 9
    ordering = ('-created_at',)

```

According to the convention. The code for `blog/templates/blog/views/list/post.html`:

```html
{% extends 'blog/base/base_site.html' %}
{% load i18n %}
{% block title %}{% translate 'Posts' %}{% endblock %}
{% block content %}
<div class="d-flex align-items-center justify-content-between">
    <h1 class="display-1">
        {% translate 'Posts' %}
    </h1>
    <a class="btn btn-primary d-flex gap-4" href="{% url 'blog:create_post' %}">
        <i class="bi bi-plus-lg"></i>
        {% translate 'New' %}
    </a>
</div>
<div class="row g-4">
    {% for post in post_list %}
    <div class="col-12 col-md-6 col-lg-4">
        {% include 'blog/includes/components/post.html' %}
    </div>
    {% empty %}
    <div class="col-12">
        <p class="display-3 text-center">
            {% translate 'No posts available.' %}
        </p>
    </div>
    {% endfor %}
</div>
{% if is_paginated %}
{% include 'blog/includes/utilties/pagination.html' %}
{% endif %}
{% endblock %}.,
```

Here is the code for `blog/views/detail.py`:

```python
from blog.models import Post
from blog.views.generic import DetailsView


class PostDetailView(DetailsView):
    model = Post

```

The code for `blog/templates/blog/views/detail/post.html`:

```html
{% extends 'blog/base/base_site.html' %}
{% load i18n %}
{% block title %}{% translate 'Post detaisl' %}{% endblock %}
{% block content %}
<div class="d-flex align-items-center justify-content-between mb-4 pb-3 border-bottom">
        <span class="lead">
            {% firstof post.user.get_full_name|capfirst post.user|capfirst %}
        </span>
    <small class="text-muted">
        {{ post.created_at|timesince }}
    </small>
</div>
{% if request.user == post.user %}
<div class="d-flex gap-4 justify-content-end">
    <a class="btn btn-warning" href="{% url 'blog:edit_post' post.id %}">
        {% translate 'Edit' %}
    </a>
    <a class="btn btn-danger" href="{% url 'blog:delete_post' post.id %}">
        {% translate 'Delete' %}
    </a>
</div>
{% endif %}
{% if post.image %}
<img src="{% url 'blog:post_image' post.id %}" alt="{{ post.title }}" class="card-img">
{% endif %}
<h1 class="display-1">
    {{ post.title }}
</h1>
<p class="fs-1 lead">
    {{ post.about }}
</p>
<p>
    {{ post.content|linebreaks }}
</p>
{% endblock %}
```

### Update View

Here is the code for `blog/views/edit.py`:

```python
from blog.models import Post
from django.contrib import messages
from django.urls import reverse_lazy
from blog.forms.main import UserEditForm, PostCreationForm
from django.contrib.auth.views import get_user_model
from blog.views.generic import MessageRequiredEditView, RequestUser, LoginRequiredMixin, AuthorityRequiredMixin

...  # Keep as it is.


class PostEditView(AuthorityRequiredMixin, MessageRequiredEditView):
    model = Post
    form_class = PostCreationForm
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Post updated successfully.'
    error_message = 'An error occurred while processing.'

```

Here is the code `blog/templates/blog/views/edit/post.html`:

```html
{% extends 'blog/views/edit/template.html' %}
{% load i18n %}
{% block title %}{% translate 'Edit Post' %}{% endblock %}
{% block page_title %}{% translate 'Edit Post' %}{% endblock %}
```

### Delete View

Here is the code for `blog/views/delete.py`:

```python
from blog.models import Post
from django.urls import reverse_lazy
from django.contrib.auth.views import get_user_model
from blog.views.generic import MessageRequiredDeletionView, RequestUser, LoginRequiredMixin, AuthorityRequiredMixin

...  # Keep as it is.


class PostDeletionView(AuthorityRequiredMixin, MessageRequiredDeletionView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Post deleted successfully.'
    error_message = 'An error occurred while processing.'

```

Here is the code for `blog/templates/blog/views/delte/post.html`:

```html
{% extends 'blog/views/delete/template.html' %}
{% load i18n %}
{% block title %}{{ block.super }} {% translate 'Post' %}{% endblock %}
{% block page_title %}{% translate 'Delete Post' %}{% endblock %}

```

Here is the code for Main views in `blog/views/main.py`:

```python
from django.views.generic import TemplateView, View
from django.http import FileResponse
from blog.views.mixins import LoginRequiredMixin
from blog.views.create import *
from blog.views.detail import *
from blog.views.edit import *
from blog.views.delete import *
from blog.views.list import *


# Create your views here.
class IndexView(TemplateView):
    template_name = 'blog/base/index.html'
    extra_context = {
        'post_list': Post.objects.all()[:9]
    }


class AboutView(TemplateView):
    template_name = 'blog/base/about.html'


class ContactView(TemplateView):
    template_name = 'blog/base/contact.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/base/dashboard.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/authentication/profile.html'


class PostImageView(View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        return FileResponse(open(post.image.url[1:], 'rb'), as_attachment=True)

```

Here is code for templates.

* `blog/templates/blog/base/index.html`:
  ```html
  {% extends 'blog/base/base_site.html' %}
  {% load i18n %}
  {% block title %}{% translate 'Home' %}{% endblock %}
  {% block main %}
  <div class="container">
      <h1 class="display-1">
          {% translate 'Blog' %}
      </h1>
      <h2 class="lead fs-2">
          {% translate 'Latest posts' %}
      </h2>
      <div class="row g-4">
          {% for post in post_list %}
          <div class="col-12 col-md-6 col-lg-4">
              {% include 'blog/includes/components/post.html' %}
          </div>
          {% empty %}
          <p class="col-12 fs-3">
              {% translate 'No post available.' %}
          </p>
          {% endfor %}
      </div>
  </div>
  {% endblock %}
  ```

* `blog/templates/blog/base/dashboard.html`
  ```html
  {% extends 'blog/base/base_site.html' %}
  {% load i18n static %}
  {% block body_attrs %}class="overflow-lg-hidden vh-lg-100"{% endblock %}
  {% block main %}
      <div class="d-flex flex-column flex-lg-row h-100">
          <div class="col-12 col-lg-3 sidebar ps-1 pe-1 pe-lg-0 pb-1">
              {% include 'blog/includes/components/sidebar.html' %}
          </div>
          <div class="col-12 col-lg-9 sidebar overflow-y-lg-auto">
              <div class="container mt-4 mt-lg-0">
                  <nav aria-label="breadcrumb" class="card card-body mb-4">
                      <ol class="breadcrumb mb-0">
                          <li class="breadcrumb-item">
                              <a href="{% url 'blog:dashboard' %}">
                                  <i class="bi bi-house"></i>
                                  {% translate 'Home' %}
                              </a>
                          </li>
                          {% block breadcrumb %}{% endblock %}
                      </ol>
                  </nav>
                  {% if messages %}
                      {% include 'blog/includes/components/messages.html' %}
                  {% endif %}
                  {% block content %}
                      <h1 class="display-1">
                          {% translate 'Welcome to Dashborad' %}
                      </h1>
                      <div class="d-flex align-items-center justify-content-between mb-4">
                          <h2 class="lead fs-2 mb-0">
                              {% translate 'My Posts' %}
                          </h2>
                          <a class="btn btn-primary d-flex gap-4" href="{% url 'blog:create_post' %}">
                              <i class="bi bi-plus-lg"></i>
                              {% translate 'New' %}
                          </a>
                      </div>
                      <div class="row g-4">
                          {% for post in user.post_set.all %}
                              <div class="col-12 col-lg-6">
                                  {% include 'blog/includes/components/post.html' %}
                              </div>
                          {% empty %}
                              <div class="col-12">
                                  <p class="display-3 text-center">
                                      {% translate 'No post available.' %}
                                  </p>
                              </div>
                          {% endfor %}
                      </div>
                  {% endblock %}
              </div>
          </div>
      </div>
  {% endblock %}
  ```

* `blog/templates/blog/base/about.html`:
  ```html
  {% extends 'blog/base/base_site.html' %}
  {% load i18n %}
  {% block title %}{% translate 'About' %}{% endblock %}
  {% block main %}
      <div class="container pt-4">
          <div class="container-fluid">
              <h1 class="display-1">
                  {% translate 'Welcome to Blog' %}
              </h1>
              <p class="col-md-8 lead fs-4">
                  {% blocktranslate %}
                      This blog app is the result of the JApp tutorial.
                  {% endblocktranslate %}
              </p>
          </div>
      </div>
  {% endblock %}

  ```

Now, we reached the end of writing views.

## Urls

Here is the code for `blog/urls.py`:

```python
from django.urls import path
from django.contrib.auth import views
from blog.forms.main import *
from blog.views.main import *
from django.urls import reverse_lazy

app_name = 'blog'
urlpatterns = [
    # Main views
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('dashbaord/', DashboardView.as_view(), name='dashboard'),

    # Posts
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/new/', PostCreationView.as_view(), name='create_post'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:id>/edit/', PostEditView.as_view(), name='edit_post'),
    path('posts/<int:id>/delete/', PostDeletionView.as_view(), name='delete_post'),
    path('posts/<int:post_id>/image/', PostImageView.as_view(), name='post_image'),

    # Custom authentication patterns
    ...  # Keep as it is.
]
```

## Templates

We need ro customize the navbar and sidebar components and add the post component. Here is the code
for `blog/templates/blog/includes/components/navbar.html`:

```html
{% load i18n %}
<nav class="navbar navbar-{{ color|default:'dark' }} bg-{{ bg_color|default:'primary' }} navbar-expand-{{ expand_at|default:'lg' }} p-3 rounded-3">
    <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'blog:index' %}">
            {% translate 'Blog' %}
        </a>
        <button class="navbar-toggler collapsed p-2 rounded-circle" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbar" aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="navbar-collapse collapse" id="navbar">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    {% url 'blog:index' as home %}
                    <a class="nav-link{% if request.path == home %} active{% endif %}" href="{{ home }}">
                        <i class="bi bi-house-fill"></i>
                        {% translate 'Home' %}
                    </a>
                </li>
                <li class="nav-item">
                    {% url 'blog:dashboard' as dashboard %}
                    <a class="nav-link{% if request.path == dashboard %} active{% endif %}" href="{{ dashboard }}">
                        <i class="bi bi-grid-1x2-fill"></i>
                        {% translate 'Dashboard' %}
                    </a>
                </li>
                <li class="nav-item">
                    {% url 'blog:about' as about %}
                    <a class="nav-link{% if request.path == about %} active{% endif %}"
                       href="{{ about }}">
                        <i class="bi bi-info-circle-fill"></i>
                        {% translate 'About' %}
                    </a>
                </li>
                <li class="nav-item">
                    {% url 'blog:contact' as contact %}
                    <a class="nav-link{% if request.path == contact %} active{% endif %}"
                       href="{{ contact }}">
                        <i class="bi bi-phone"></i>
                        {% translate 'Contact' %}
                    </a>
                </li>
                <li class="nav-item">
                    {% url 'blog:post_list' as post_list %}
                    <a class="nav-link{% if request.path == post_list %} active{% endif %}"
                       href="{{ post_list }}">
                        <i class="bi bi-list"></i>
                        {% translate 'Posts' %}
                    </a>
                </li>
            </ul>
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'blog:profile' %}">
                        <i class="bi bi-person-circle"></i>
                        {% translate 'Profile' %}
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="https://github.com/youzarsiph/JApp.git">
                        <i class="bi bi-github"></i>
                        {% translate 'Github' %}
                    </a>
                </li>
                <li class="nav-item">
                    {% if request.user.is_authenticated %}
                    <a class="nav-link" href="{% url 'blog:logout' %}">
                        <i class="bi bi-power"></i>
                        {% translate 'Logout' %}
                    </a>
                    {% else %}
                    <a class="nav-link" href="{% url 'blog:login' %}">
                        <i class="bi bi-box-arrow-in-right"></i>
                        {% translate 'Login' %}
                    </a>
                    {% endif %}
                </li>
            </ul>
        </div>
    </div>
</nav>
```

Here is the code for `blog/templates/blog/includes/components/sidebar.html`:

```html
{% load i18n %}
<nav class="navbar navbar-{{ color|default:'dark' }} bg-{{ bg_color|default:'primary' }} navbar-expand-{{ expand_at|default:'lg' }} align-items-lg-start h-100 rounded-3"
     aria-label="Side bar">
    <div class="container-fluid flex-lg-column align-items-lg-start h-100 w-100">
        <button class="navbar-toggler rounded-circle p-2" type="button" data-bs-toggle="offcanvas"
                data-bs-target="#sidebar"
                aria-controls="sidebar">
            <span class="navbar-toggler-icon"></span>
        </button>
        <a class="navbar-brand me-0" href="#">
            {% translate 'Dashboard' %}
        </a>
        <div class="navbar-nav d-lg-none">
            <a class="nav-link px-3 p-lg-2{% if request.path == profile %} active{% endif %}"
               href="{% url 'blog:profile' %}">
                <i class="bi bi-person-circle"></i>
            </a>
        </div>
        <div class="offcanvas offcanvas-end text-white bg-{{ bg_color|default:'primary' }}" tabindex="-1" id="sidebar"
             aria-labelledby="sidebarLabel">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title" id="sidebarLabel">
                    {% translate 'Dashboard' %}
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                        aria-label="Close"></button>
            </div>
            <div class="offcanvas-body d-flex flex-column justify-content-between h-100">
                <ul class="navbar-nav flex-lg-column w-100">
                    <li class="nav-item">
                        {% url 'blog:dashboard' as dashboard %}
                        <a class="nav-link d-flex gap-4{% if request.path == dashboard %} active{% endif %}"
                           href="{{ dashboard }}">
                            <i class="bi bi-gear-fill"></i>
                            {% translate 'Dashboard' %}
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link d-flex gap-4" href="{% url 'blog:create_post' %}">
                            <i class="bi bi-plus"></i>
                            {% translate 'New Post' %}
                        </a>
                    </li>
                </ul>
                <ul class="navbar-nav flex-column">
                    <li class="nav-item">
                        {% url 'blog:profile' as profile %}
                        <a class="nav-link d-flex gap-4{% if request.path == profile %} active{% endif %}"
                           href="{{ profile }}">
                            <i class="bi bi-person-circle"></i>
                            {% translate 'Account' %}
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link d-flex gap-4" href="{% url 'blog:logout' %}">
                            <i class="bi bi-power"></i>
                            {% translate 'Log out' %}
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</nav>
```

Here is the code for `blog/templates/blog/includes/components/post.html`:

```html
{% load i18n %}
<div class="card">
    {% if post.image %}
    <img src="{% url 'blog:post_image' post.id %}" alt="{{ post.title }}" class="card-img-top">
    {% endif %}
    <div class="card-body">
        <div class="card-title d-flex align-items-center justify-content-between">
            <h3 class="mb-0 lead fs-3">
                {{ post.title }}
            </h3>
            <div class="dropdown">
                <a href="#" data-bs-toggle="dropdown">
                    <i class="bi bi-three-dots"></i>
                </a>
                <div class="dropdown-menu shadow rounded-3">
                    <div class="dropdown-header">
                        {% translate 'Post Menu' %}
                    </div>
                    <a class="dropdown-item d-flex gap-4" href="{% url 'blog:post_detail' post.id %}">
                        <i class="bi bi-eye"></i>
                        {% translate 'Details' %}
                    </a>
                    {% if request.user == post.user %}
                    <a class="dropdown-item d-flex gap-4" href="{% url 'blog:edit_post' post.id %}">
                        <i class="bi bi-pencil"></i>
                        {% translate 'Edit' %}
                    </a>
                    <a class="dropdown-item d-flex gap-4" href="{% url 'blog:delete_post' post.id %}">
                        <i class="bi bi-trash"></i>
                        {% translate 'Delete' %}
                    </a>
                    {% endif %}
                </div>
            </div>
        </div>
        <div class="card-text">
            <p>
                {{ post.about }}
            </p>
        </div>
    </div>
    <div class="card-footer d-flex align-items-center justify-content-between">
        <div class="d-flex align-items-center gap-4">
            <div class="d-flex align-items-center justify-content-center px-3 py-2 bg-primary rounded-3">
                <i class="bi bi-person-fill text-white"></i>
            </div>
            <span class="lead">
                {% firstof post.user.get_full_name|capfirst post.user.username|capfirst %}
            </span>
        </div>
        <small class="text-muted">
            {{ post.created_at|timesince }}
        </small>
    </div>
</div>
```

Now we are ready to see the result. Run the server and enjoy.

```shell
python manage.py runserver
```

I hope that you find this useful. Thanks for your time.