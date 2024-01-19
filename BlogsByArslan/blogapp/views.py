from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from django.views.generic import UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def blogs(request):
#     """
#     The blogs function is a view that displays all blog posts.
#     It takes in the request object and returns an HTML page with all of the blog posts.
    
#     :param request: Get the request from the user
#     :return: renders to the blog.html page
#     """
#     posts = BlogPost.objects.all()
#     posts = BlogPost.objects.filter().order_by('-dateTime')
#     return render(request, "blog.html", {'posts':posts})
def blogs(request):
    """
    The blogs function is a view that displays all blog posts.
    It takes in the request object and returns an HTML page with all of the blog posts.

    :param request: Get the request from the user
    :return: renders to the blog.html page
    """
    posts_list = BlogPost.objects.all().order_by('-dateTime')
    
    paginator = Paginator(posts_list, 5)  # Show 5 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog.html", {'posts': posts})

def blogs_comments(request, slug):
    """
    The blogs_comments function is used to display the comments for a particular blog post.
    It takes in two parameters, request and slug. The function first gets the blog post using
    the slug parameter and then gets all of the comments associated with that blog post. If 
    the method is POST, it creates a new comment object with user as current user, content as 
    content from form input field and saves it to database.
    
    :param request: Get information from the user
    :param slug: Filter the blogpost object by slug
    :return: renders to the blog_comments.html page
    """
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','')
        blog_id =request.POST.get('blog_id','')
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
    return render(request, "blog_comments.html", {'post':post, 'comments':comments})

def Delete_Blog_Post(request, slug):
    """
    The Delete_Blog_Post function is a view that allows the user to delete a blog post.
    The function takes in two arguments, request and slug. The request argument is an HTTP GET or POST
    request sent by the client to the server. The slug argument is used as an identifier for each blog post.
    
    :param request: Get the data from the form, and then we use posts
    :param slug: Get the specific blog post that we want to delete
    :return: renders to the delete_blog_post.html page
    """
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts':posts})

@login_required(login_url = '/login')
def add_blogs(request):
    """
    Login Required
    The add_blogs function is used to add a blog post.
    It takes in the request and returns the rendered template of add_blogs.html
    
    :param request: Get the data from the form
    :return: renders to the add_blogs.html page
    """
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html",{'obj':obj, 'alert':alert})
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image']

def search(request):
    """
    The search function allows the user to search for a blog post by title.
    The function takes in a request and returns the searched value, as well as all of the blogs that contain that value.
    
    :param request: Get the request from the user
    :return: The searched term and the blogs that contain it
    """
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "search.html", {'searched':searched, 'blogs':blogs})
    else:
        return render(request, "search.html", {})