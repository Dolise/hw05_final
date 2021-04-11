from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from django.urls import reverse

from yatube.settings import PAGINATOR_PER_PAGE

from .models import Post, Group, User, Comment, Follow


def index(request):
    """Return rendered main page with last 10 posts."""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, PAGINATOR_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    """Return rendered group page with posts."""
    group = get_object_or_404(Group, slug=slug)
    posts_list = Post.objects.all().filter(group=group)
    paginator = Paginator(posts_list, PAGINATOR_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page})


@login_required(login_url='/auth/login/')
def new_post(request):
    """Return rendered page for adding new post and add post to DB."""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            author = request.user
            image = form.cleaned_data['image']
            post = Post(author=author, group=group, text=text, image=image)
            post.save()
            return redirect('index')
        return render(request, 'new_post.html', {'form': form,
                                                 'url': '/new/',
                                                 })
    return render(request, 'new_post.html', {'form': form,
                                             'url': '/new/',
                                             })


def profile(request, username):
    """Return rendered page of user profile."""
    get_object_or_404(User, username=username)
    author = User.objects.get(username=username)

    posts_list = Post.objects.all().filter(author=author)
    paginator = Paginator(posts_list, PAGINATOR_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    follows = Follow.objects.filter(user=author).count()
    followers = Follow.objects.filter(author=author).count()
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, author=author).exists():
            following = True

    return render(request, 'profile.html',
                  {'page': page,
                   'author': author,
                   'posts_list': posts_list,
                   'following': following,
                   'follows': follows,
                   'followers': followers,
                   })


def post_view(request, username, post_id):
    """Return rendered page of certain post."""
    get_object_or_404(Post, id=post_id)
    author = User.objects.get(username=username)
    posts_list = Post.objects.all().filter(author=author)
    author = User.objects.get(username=username)
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()
    follows = Follow.objects.filter(user=author).count()
    followers = Follow.objects.filter(author=author).count()
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, author=author).exists():
            following = True
    return render(request, 'post.html', {'author': author, 'post': post,
                                         'posts_list': posts_list,
                                         'form': comment_form,
                                         'comments': comments,
                                         'following': following,
                                         'follows': follows,
                                         'followers': followers,
                                         })


@login_required(login_url='/auth/login/')
def post_edit(request, username, post_id):
    """Return rendered page of post edit and save changes to DB."""
    if not request.user.is_authenticated or request.user.username != username:
        return redirect('post', username=username, post_id=post_id)
    get_object_or_404(Post, id=post_id)
    post = Post.objects.get(id=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post
                    )

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post', username=username, post_id=post_id)
        return render(request, 'new_post.html',
                      {'form': form,
                       'url': f'/{username}/{post_id}/edit/',
                       'post': post})
    return render(request, 'new_post.html',
                  {'form': form,
                   'url': f'/{username}/{post_id}/edit/',
                   'post': post})


@login_required(login_url='/auth/login/')
def add_comment(request, username, post_id):
    """Is used to add comment to DB."""
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            text = form.cleaned_data['text']
            author = request.user
            post = Post.objects.get(id=post_id)
            comment = Comment(text=text, author=author, post=post)
            comment.save()
            return redirect(
                reverse(
                    'post',
                    kwargs={
                        'username': username,
                        'post_id': post_id
                    }))
        return redirect(
            reverse(
                'post',
                kwargs={
                    'username': username,
                    'post_id': post_id
                }
            )
        )
    return redirect(reverse('post', kwargs={
        'username': username,
        'post_id': post_id,
    }))


@login_required(login_url='/auth/login/')
def follow_index(request):
    """Return rendered page with posts of users followings."""
    follows = Follow.objects.filter(user=request.user).values_list('author')
    posts = Post.objects.filter(author__in=follows)
    paginator = Paginator(posts, PAGINATOR_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page})


@login_required(login_url='/auth/login/')
def profile_follow(request, username):
    """Is used to add profile follow in DB."""
    author = User.objects.get(username=username)
    if Follow.objects.filter(user=request.user, author=author).exists()\
            or request.user.username == username:
        return redirect(reverse('index'))
    Follow.objects.create(user=request.user, author=author)
    return redirect(reverse('profile', kwargs={'username': username}))


@login_required(login_url='/auth/login/')
def profile_unfollow(request, username):
    """Is used to add profile unfollow to DB."""
    author = User.objects.get(username=username)
    if Follow.objects.filter(user=request.user, author=author).exists()\
            or author.username == username:
        Follow.objects.get(user=request.user, author=author).delete()
        return redirect(reverse('profile', kwargs={'username': username}))
    return redirect(reverse('index'))


def page_not_found(request, exception):
    """Return rendered page of 404 error."""
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    """Return rendered page of 500 error."""
    return render(
        request,
        'misc/500.html',
        status=500
    )
