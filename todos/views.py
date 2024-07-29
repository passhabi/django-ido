from datetime import datetime

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from todos.forms import TodolistForm
from todos.models import Todolist
from ido.helpers.profile import ProfileManager


# Create your views here.
def homepage(request):
    return render(request, "index.html")


def signin(request):
    if request.method == "GET":
        return render(request, "sign-in.html")

    # if request.method == "POST":
    user = authenticate(
        request,
        username=request.POST["username"],
        password=request.POST["password"],
    )
    if user:
        login(request, user)
        return redirect("list_todos")
    else:
        return render(
            request,
            "sign-in.html",
            {
                "errors": [
                    "The combination of username and password do not exist.",
                ]
            },
        )


def signup(request):
    # (GET)
    if request.method == "GET":
        return render(request, template_name="sign-up.html")

    # (POST) Registering the new user:
    profile_mgr = ProfileManager(request)

    if profile_mgr.check_password(request.POST["password1"], request.POST["password2"]):  # if there was an error:
        return render(
            request,
            template_name="sign-up.html",
            context={"values": profile_mgr.get_profile_as_dict, 'is_valid': profile_mgr.get_html_validation_dict},
        )

    if profile_mgr.dose_the_user_exists():
        return render(
            request,
            template_name="sign-up.html",
            context={'values': profile_mgr.get_profile_as_dict, 'is_valid': profile_mgr.get_html_validation_dict},
        )

    user = profile_mgr.create_the_user()

    login(request, user)
    return redirect("homepage")


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("homepage")
    return redirect("homepage")


@login_required(login_url="login")
def order_it_by(request):
    user = User.objects.get(username=request.user)

    user.usersetting.order_by = request.POST['orderby'][0]  # take the first letter. e.g. title >>> 't'
    user.usersetting.save()

    return list_todos(request)


@login_required(login_url="login")
def reverse_the_order(request):
    user = User.objects.get(username=request.user)
    user.usersetting.is_descending = not user.usersetting.is_descending
    user.usersetting.save()

    return list_todos(request)


@login_required(redirect_field_name="login")
def list_todos(request):
    user = User.objects.get(username=request.user)
    user_view_settings = user.usersetting

    todo_items = Todolist.objects.filter(user=request.user, completion_time=None)

    # add view settings to template:
    query_str = '-'
    if user_view_settings.is_descending:
        query_str = ''
    query_str += user_view_settings.ORDER_BY_CHOICES[user_view_settings.order_by]

    todo_items = todo_items.order_by(query_str)  # sort items by query_set

    return render(
        request,
        r"list_todos.html",
        {"todo_items": todo_items,
         "user_view_settings": user_view_settings, },
    )


@login_required
def detailed_todo(request, id):
    todo = get_object_or_404(Todolist, pk=id, user=request.user)

    if request.method == "GET":
        request.previous_path = request.META['HTTP_REFERER']  # cache the previous path
        return render_edit_page(request, todo)

    # POST:
    request.META['HTTP_REFERER'] = request.POST['previous_path']  # fetch the previous path

    if request.POST["button"] == "complete_button":
        return make_as_completed(request, id)

    if request.POST["button"] == "save_button":
        todolist_form = TodolistForm(request.POST, instance=todo)
        todolist_form.save()

        todo = get_object_or_404(Todolist, pk=id, user=request.user)

        request.previous_path = request.META['HTTP_REFERER']  # cache the previous path
        return render_edit_page(request, todo, True)

    if request.POST["button"] == "delete":
        todolist_form = TodolistForm(request.POST, instance=todo)
        todo.delete()
        return redirect(request.POST['previous_path'])


def render_edit_page(request, todo, saved: bool = False):
    if todo.priority:
        todo.__dict__["priority_radio_select" + str(todo.priority)] = (
            "checked"  # this is the html radio tag 'checked'.
        )
    todo.__dict__["category_option" + str(todo.category)] = (
        "selected"  # this is the html tag.
    )
    return render(
        request, "edit.html", context={"todo": todo, "has_been_saved": saved}
    )


@login_required
def add_todo(request):
    if request.method == "GET":
        # todo: send categories to template.
        return render(request, "add_todo.html")

    # bug: repeated add? use ratelimit?
    newitem = TodolistForm(request.POST)
    newitem.save(commit=False).user = request.user
    newitem.save()

    return render(
        request, "add_todo.html", context={"added_todo": request.POST["title"]}
    )


@login_required
def delete_todo(request, id):
    if request.method == "GET":
        return redirect("list_todos")

    todo = get_object_or_404(Todolist, id=id, user=request.user)
    todo.delete()

    return redirect("list_todos")


@login_required
def list_completed_todos(request):
    if request.method == "GET":
        completed_todos = Todolist.objects.filter(completion_time__isnull=False, user_id=request.user).order_by(
            '-completion_time')
        completed_todos = list(completed_todos)
        return render(request, 'completed.html', context={'completed_todos': completed_todos})


@login_required
def un_complete_todos(request, id):
    todo = Todolist.objects.filter(id=id, user=request.user)
    todo.update(completion_time=None)

    return redirect(request.META.get('HTTP_REFERER'))


def make_as_completed(request, id):
    todo = get_object_or_404(Todolist, pk=id, user=request.user)

    todo.completion_time = datetime.now()
    todo.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request):
    if request.method == "GET":
        return render(request, 'user_profile.html', context={'user': request.user})

    # if it is a POST:
    profile_mgr = ProfileManager(request)

    user = profile_mgr.update_the_user(password2=request.POST.get('password2'))

    if user:
        return render(request, 'user_profile.html',
                      context={'user': user,
                               'is_error_in_update': True})
    else:
        return render(request, 'user_profile.html',
                      context={'user': request.user,
                               'is_valid': profile_mgr.get_html_validation_dict})
