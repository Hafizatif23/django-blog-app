from django.shortcuts import render,redirect
from .models import Post,Comment
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):

    posts = Post.objects.order_by('-date')
    return render(request, 'GeneralBlogApp/home.html', {'posts': posts})


def post_detail(request, post_id):
    post = Post.objects.get(id = post_id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
             return redirect('post_detail')
        text = request.POST.get('comment')

        if not text:
            return redirect('post_detail', post_id= post.id)

        Comment.objects.create(post=post, author=request.user, text= text)
        return redirect('post_detail', post_id = post.id)

    comments = post.comment_set.all()
    return render(request, 'GeneralBlogApp/post_detail.html', {'post':post, 'comments':comments})

@login_required
def write_post(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if not title or not content:
            return redirect('home')

        Post.objects.create(title= title, author=request.user, content=content, category = category, image = image)
        return redirect('home')

    return render(request, 'GeneralBlogApp/write_post.html')

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id= post_id)

    if request.method == 'POST':
        if post.author != request.user:
            return redirect('post_detail', post_id = post.id)
        
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.category = request.POST.get('category')
        new_image = request.FILES.get('image')

        if new_image:
            post.image = new_image

        if not post.title or not post.content:
            return redirect('home')
        
        post.save()

        return redirect('home')
    return render(request, 'GeneralBlogApp/edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id = post_id)

    if post.author != request.user:
         return redirect('post_detail', post_id = post.id)
    
    if request.method == 'POST':
        post.delete()
    
    return redirect('home')
