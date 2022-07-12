from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
import bcrypt


def root(request):
    return redirect('/home')


# helper function for Filtering
def is_valid(param):
    return param != '' and param is not None


# home :)
def home(request):
    recipes = Recipe.objects.all()

    # Search part
    if request.method == 'GET':
        if request.GET.get('search') != '' and request.GET.get('search') is not None:
            recipes = Recipe.objects.filter(
                Q(title__icontains=request.GET['search'])
                | Q(desc__icontains=request.GET['search'])
                | Q(chef__user_name__icontains=request.GET['search'])
                | Q(ingredient__name__icontains=request.GET['search'])
            ).distinct()

    # Filter part
    if request.method == 'POST':
        filter = request.POST.getlist('filter')
        q = Q()
        for item in filter:
            if item == 'dairy':
                dairy = ['milk', 'cheese', 'yogurt',
                         'cream', 'butter', 'whey', 'casein']
                for d in dairy:
                    q |= Q(ingredient__name__icontains=d)
            q |= Q(ingredient__name__icontains=item)

        recipes = Recipe.objects.exclude(q)

    if 'user' in request.session:
        context = {
            'user': Chef.objects.get(id=request.session['user']),
            'recipes': recipes,
        }
        return render(request, 'home.html', context)
    else:
        context = {
            'recipes': recipes,
        }
        return render(request, 'home.html', context)


# register a user
def register(request):
    form = create_user()
    return render(request, 'register.html', {'form': form})


# login a user
def login_view(request):
    return render(request, 'login.html')


# gettin the user in
def userin_home(request):
    if request.method == 'POST':
        # registeration
        if request.POST['form'] == "register":
            error = Chef.objects.basic_validator(request.POST)

            if len(error) > 0:
                for error_message in error.values():
                    messages.error(request, error_message)
                return redirect('/register')
            else:
                form = create_user(request.POST, request.FILES)
                if form.is_valid():
                    user = form.save(commit=False)
                    pw_hash = bcrypt.hashpw(
                        request.POST['password'].encode(), bcrypt.gensalt()).decode()
                    user.password = pw_hash
                    user.save()
                    request.session['user'] = user.id
                    return redirect('/home')

        # ligin
        if request.POST['form'] == "login":
            user = Chef.objects.filter(email=request.POST['email'])
            if user:
                if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
                    request.session['user'] = user[0].id
                    return redirect('/home')
                else:
                    messages.error(request, "the password is not correct")
                    return redirect('/home')
            else:
                messages.error(request, "the user email havn't registered yet")
            return redirect('/home')
    return redirect('/home')


# display chefs profiles
def profile(request, id):
    if 'user' in request.session:
        context = {
            'user': Chef.objects.get(id=request.session['user']),
            'chef': Chef.objects.get(id=id),
        }
        return render(request, 'profile.html', context)
    else:
        context = {
            'chef': Chef.objects.get(id=id),
        }
        return render(request, 'profile.html', context)


# edit chef profile
def edit_profile(request):
    if 'user' in request.session:
        user = Chef.objects.get(id=request.session['user'])
        if request.method == 'POST':
            form = create_user(request.POST, request.FILES, instance=user)
            if form.is_valid():
                user = form.save()
                user.user_name = request.POST['user_name']
                user.email = request.POST['email']
                password = bcrypt.hashpw(
                    request.POST['password'].encode(), bcrypt.gensalt()).decode()
                user.password = password
                user.save()

                return redirect(f'/profile/{user.id}')
        else:
            form = create_user(instance=user)
            context = {
                'user': Chef.objects.get(id=request.session['user']),
                'form': form,
            }
            return render(request, 'edit_profile.html', context)
    return redirect('/home')


# display all registered chefs
def chefs(request):
    if 'user' in request.session:
        context = {
            'user': Chef.objects.get(id=request.session['user']),
            'chefs': Chef.objects.all(),
        }
        return render(request, 'all_chefs.html', context)
    else:
        context = {
            'chefs': Chef.objects.all(),
        }
        return render(request, 'all_chefs.html', context)


# add a recipeا
def add_recipe(request):
    if 'user' in request.session:
        if request.method == "POST":
            form = RecipeForm(request.POST, request.FILES)
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.chef = Chef.objects.get(id=request.session['user'])
                recipe.save()
                for ingredient_id in request.POST.getlist('ingredients'):
                    try:
                        ingredient = Ingredient.objects.get(id=ingredient_id)
                        recipe.ingredient.add(ingredient)
                    except:
                        ingredient = Ingredient.objects.create(
                            name=ingredient_id)
                        recipe.ingredient.add(ingredient)

                context = {
                    'user': Chef.objects.get(id=request.session['user']),
                    'recipe': recipe,
                }
                return render(request, "recipe.html", context)
        else:
            form = RecipeForm()
            context = {
                'user': Chef.objects.get(id=request.session['user']),
                'form': form,
                "ingredients": Ingredient.objects.all(),
            }
        return render(request, "add_recipe.html", context)
    else:
        return redirect('/home')


# edit a recipe
def edit(request, id):
    if 'user' in request.session:
        recipe = Recipe.objects.get(id=id)
        if request.method == 'POST':
            form = RecipeForm(request.POST, request.FILES, instance=recipe)
            if form.is_valid():
                recipe = form.save()
                # recipe.img = request.FIELS['img']
                recipe.title = request.POST['title']
                recipe.desc = request.POST['desc']
                recipe.ingredient.remove(*recipe.ingredient.all())

                for ingredient_id in request.POST.getlist('ingredients'):
                    try:
                        ingredient = Ingredient.objects.get(id=ingredient_id)
                        recipe.ingredient.add(ingredient)
                    except:
                        ingredient = Ingredient.objects.create(
                            name=ingredient_id)
                        recipe.ingredient.add(ingredient)
                recipe.save()
            context = {
                'user': Chef.objects.get(id=request.session['user']),
                'recipe': recipe,
            }
            return render(request, "recipe.html", context)
        else:
            form = RecipeForm(instance=recipe)
            context = {
                'user': Chef.objects.get(id=request.session['user']),
                'recipe': Recipe.objects.get(id=id),
                'form': form,
                'ingredients': Ingredient.objects.all(),
            }
            return render(request, 'edit_recipe.html', context)
    else:
        return redirect('/home')


# delete a recipe
def delete(request, id):
    if 'user' in request.session:
        recipe = Recipe.objects.get(id=id)
        recipe.delete()
    return redirect('/home')


# display recipe
def recipe_detail(request, id):
    if 'user' in request.session:
        context = {
            'user': Chef.objects.get(id=request.session['user']),
            'recipe': Recipe.objects.get(id=id),
        }
        return render(request, 'recipe.html', context)
    else:
        context = {
            'recipe': Recipe.objects.get(id=id),
        }
        return render(request, 'recipe.html', context)


# logout
def logout(request):
    request.session.flush()
    return redirect('/home')


# 404 page
def handler404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response
