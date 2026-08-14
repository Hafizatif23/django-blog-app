from django.shortcuts import render,redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Post,Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer


def home(request):

    posts = Post.objects.order_by('-date')
    return render(request, 'GeneralBlogApp/home.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, id = pk)

    if request.method == 'POST':
        if not request.user.is_authenticated:
             return redirect('login')
        text = request.POST.get('comment')

        if not text:
            return redirect('post_detail', pk= post.id)

        Comment.objects.create(post=post, author=request.user, text= text)
        return redirect('post_detail', pk = post.id)

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
def edit_post(request, pk):
    post = get_object_or_404(Post, id= pk)

    if request.method == 'POST':
        if post.author != request.user:
            return redirect('post_detail', pk = post.id)
        
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
def delete_post(request, pk):
    post = get_object_or_404(Post, id = pk)

    if post.author != request.user:
         raise PermissionDenied
    
    if request.method == 'POST':
        post.delete()
    
    return redirect('home')

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if comment.author != request.user and comment.post.author != request.user:
        return redirect('post_detail', pk = comment.post.id)
    if request.method == 'POST':
        comment.delete()
    return redirect('post_detail', pk = comment.post.id)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'GeneralBlogApp/signup.html', {'form': form})
@method_decorator(csrf_exempt, name='dispatch')
class PostListApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        posts = Post.objects.order_by('-date')
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)


    def post(self, request):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(author= request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        if post.author != request.user:
            return Response(
                {'detail':'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        if post.author != request.user:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        if post.author != request.user:
            return Response(
                {'detail':'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        comments = Comment.objects.order_by('-date')
        serializer = CommentSerializer(comments, many= True)
        return Response(serializer.data)

    def post(self, request):
            serializer = CommentSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(author= request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, pk):
        post = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        if comment.author != request.user:
            return Response(
                {'detail':'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        if comment.author != request.user and comment.post.author != request.user :
            return Response(
                {'detail':'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

