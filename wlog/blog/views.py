from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import ProfileForm, SignInForm, PostCreationForm
from .models import Profile, Post

# Create your views here.
@login_required(login_url="sign_in")
def home(request, page=1):
    POSTS_PER_PAGE = 5

    posts_start_index = (page - 1) * POSTS_PER_PAGE 

    posts = Post.objects.all().order_by('-date').values()
    nPosts = Post.objects.count()

    posts = posts[posts_start_index:min(len(posts), posts_start_index + POSTS_PER_PAGE) ]
    return render(request, "feed.html", {
        "posts": posts,
        "pages": [x for x in range(1, (nPosts // POSTS_PER_PAGE) + 2)]
    })


def sign_in(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": SignInForm(),
            "error": ""
        })
    elif request.method == "POST":
        user = authenticate(username=request.POST["nickname"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "signin.html", {
                "form": SignInForm(),
                "error": "User or password incorrect"
                })
        

def sign_up(request):
    form = UserCreationForm()
    error = ""
    if request.method == "GET":
        return render(request, "signup.html", {
            "form": form,
            "error": error
        })
    elif request.method == "POST":
        if request.POST["password1"] != request.POST["password2"]:
            error = "Passwords do not match"
            return render(request, "signup.html", {
                "form": form,
                "error": error
            })
        else:
            exists = User.objects.filter(username=request.POST["username"]).exists()

            if exists:
                error = "User Already exists"
                return render(request, "signup.html", {
                    "form": form,
                    "error": error
                })
            else:
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                profile = Profile.objects.create(user = user)
                return redirect("sign_in")
                


@login_required(login_url="sign_in")
def sign_out(request):
    logout(request)
    return render(request, "signout.html")


def about(request):
    return render(request, "about.html")


@login_required(login_url="sign_in")
def myaccount(request):
    profile = Profile.objects.get(user = request.user)
    if request.method == "GET":
        return render(request, "myaccount.html", {
            "form": ProfileForm(instance=profile),
            "profile_image": profile.picture
        })
    else:
        form = ProfileForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.name = request.POST["name"]
            profile.last_name = request.POST["last_name"]
            profile.location = request.POST["location"]

            if request.FILES.get('picture') != None:
                    profile.picture = request.FILES.get('picture')

            profile.save()


            return render(request, "myaccount.html", {
                "form": ProfileForm(instance=profile),
                "profile_image":profile.picture,
                "message": "Profile updated!"
            })
        else:
            return render(request, "myaccount.html", {
                "form": ProfileForm(instance=profile),
                "profile_image":profile.picture,
                "error_message": "Something went wrong :("
            })
        

@login_required(login_url="sign_in")
def create_post(request):
    if request.method == "GET":
        return render(request, "createpost.html", {
            "form":PostCreationForm()
        })
    else:
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = __current_profile__(request)
            new_post.save()
            form.save_m2m()
            
        return redirect("list_posts", user_id=request.user.id)


@login_required(login_url="sign_in")
def list_posts(request, user_id = None):
    my_user = User.objects.get(id = user_id)
    posts = Post.objects.filter(created_by_id = my_user.id)
    context = {
        "my_user":my_user,
        "posts": posts
    }
    return render(request, "listposts.html", context)


@login_required(login_url="sign_in")
def post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    return render(request, "post.html", {
        "post":post
    })


@login_required(login_url="sign_in")
def search_user(request):
    if request.method == "POST":
        term = "%" + request.POST.get("id_term") + "%"
        users = User.objects.raw("select * from auth_user where username like %s", [term])
        profiles = set()
        for u in users:
            profiles.add(Profile.objects.get(user=u))

        name_profiles = Profile.objects.raw("select * from blog_profile where name like %s or last_name like %s", [term, term])
        for np in name_profiles:
            profiles.add(np)
            
        return render(request, "searchuser.html", {
            "searched": term,
            "profiles": list(profiles)
        })
    else:
        return render(request, "searchuser.html")



def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.get(user = user)

    return render(request, "profile.html", {
        "profile": profile
    })

def __current_profile__(request):
    p = Profile.objects.get(user = request.user)
    return p
