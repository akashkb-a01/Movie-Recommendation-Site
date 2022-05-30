from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from .forms import ProfileForm
from .models import Movie, Profile, MyList, MyRating
from django.db.models import Q, Case, When
from django.http import HttpResponseRedirect


import pandas as pd


from django.http import Http404

class Home(View):
    def get(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/profile/')
        return render(request,'index.html')

@method_decorator(login_required,name='dispatch')
class ProfileList(View):
    
    def get(self,request,*args, **kwargs):

        profiles=request.user.profiles.all()

        return render(request,'profileList.html',{
            'profiles':profiles
        })


@method_decorator(login_required,name='dispatch')
class ProfileCreate(View):
    def get(self,request,*args, **kwargs):
        form=ProfileForm()

        return render(request,'profileCreate.html',{
            'form':form
        })

    def post(self,request,*args, **kwargs):
        form=ProfileForm(request.POST or None)

       
        if form.is_valid():
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect(f'/watch/{profile.uuid}')

        return render(request,'profileCreate.html',{
            'form':form
        })

@method_decorator(login_required,name='dispatch')
class Watch(View):
    def get(self,request,profile_id,*args, **kwargs):
        try:
            profile=Profile.objects.get(uuid=profile_id)
            mylist=MyList.objects.all().filter(profile=profile,watch=True).values('movie_id')
            mymovieslist=Movie.objects.filter(id__in=mylist.values_list('movie_id'))
            if profile.age_limit == 'Kids':
                movies=Movie.objects.filter(adult=False).order_by('-vote_count')
            else:
                movies=Movie.objects.order_by('-vote_count')              
            
            query = request.GET.get('q')

            if query:
                query_list = movies.filter(Q(title__icontains=query)).distinct()
                return render(request, 'searchList.html', {
                    'movies': query_list,
                    'search_query':query,
                    'profile':profile
                })
            # movies = sorted(Movie.objects.order_by('-vote_count'), key=lambda a: 'Sci-Fi' in a.genre, reverse=True)
            Genres=['Action','Adventure','Animation','Comedy','Crime','Drama','Family','Fantasy','History','Horror','Music','Mystery','Romance','Sci-Fi','Thriller','War','Western']
            mo = {}
            recommendations = recommend(profile_id)
            if recommendations:
                recommendations=recommendations[0:7]
            myList=mymovieslist[0:7]
            popularMovies=movies.order_by('-popularity')[0:7]
            topRated=movies.order_by('-vote_average')[0:7]
            for genres in Genres:
                mo[genres] = movies.filter(genre__icontains=genres)[0:7]
            try:
                showcase=movies[0]
            except :
                showcase=None
            

            if profile not in request.user.profiles.all():
                return redirect(to='core:profile_list')
            return render(request,'movieList.html',{
            'recommendations':recommendations,
            'myList':myList,
            'popular':popularMovies,
            'top':topRated,
            'show_case':showcase,
            'genrelist':mo,
            'profile':profile
            })
        except Profile.DoesNotExist:
            return redirect(to='core:profile_list')

@method_decorator(login_required,name='dispatch')
class genreList(View):
    def get(self,request,profile_id,movie_genre,index_freq=100,*args, **kwargs):
        try:
            profile=Profile.objects.get(uuid=profile_id)
            # movies=Movie.objects.filter(genre='Comedy, Music').order_by('-popularity')
            if profile.age_limit == 'Kids':
                movies = Movie.objects.filter(adult=False).filter(genre__icontains=movie_genre).order_by('-vote_count')
            else:
                movies = Movie.objects.all().filter(genre__icontains=movie_genre).order_by('-vote_count')
            
            query = request.GET.get('q')

            if query:
                query_list = movies.filter(Q(title__icontains=query)).distinct()
                return render(request, 'searchList.html', {
                    'movies': query_list,
                    'search_query':query,
                    'profile':profile
                })
            try:
                showcase=movies[0]
            except :
                showcase=None
            
            return render(request,'genreList.html',{
            'movies':movies[0:index_freq],
            'show_case':showcase,
            'movie_genre':movie_genre,
            'profile':profile
            })
        except Profile.DoesNotExist:
            return redirect(to='core:profile_list')


@method_decorator(login_required,name='dispatch')
class ShowMovieDetail(View):
    def post(self,request,profile_id,movie_id,*args, **kwargs):
        try:

            profile=Profile.objects.get(uuid=profile_id)
            movie=Movie.objects.get(id=movie_id)

            temp = list(MyList.objects.all().values().filter(movie_id=movie_id,profile=profile))
            if temp:
                update = temp[0]['watch']
            else:
                update = False
            if request.method == "POST":
                # For my list
                if 'watch' in request.POST:
                    watch_flag = request.POST['watch']
                    if watch_flag == 'on':
                        update = True
                    else:
                        update = False
                    if MyList.objects.all().values().filter(movie_id=movie_id,profile=profile):
                        MyList.objects.all().values().filter(movie_id=movie_id,profile=profile).update(watch=update)
                    else:
                        q=MyList(profile=profile,movie=movie,watch=update)
                        q.save()
                    if update:
                        messages.success(request, "Movie added to your list!")
                    else:
                        messages.success(request, "Movie removed from your list!")

                # For rating
                else:
                    rate = request.POST['rating']
                    if MyRating.objects.all().values().filter(movie_id=movie_id,profile=profile):
                        MyRating.objects.all().values().filter(movie_id=movie_id,profile=profile).update(rating=rate)
                    else:
                        q=MyRating(profile=profile,movie=movie,rating=rate)
                        q.save()

                    messages.success(request, "Rating has been submitted!")

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            out = MyRating.objects.get(profile=profile,movie_id=movie_id).values()

            # To display ratings in the movie detail page
            movie_rating=0
            rate_flag=False
            if out:
                movie_rating = out['rating']
                rate_flag = True
        
            # for each in out:
            #     if each['movie_id'] == movie_id:
            #         movie_rating = each['rating']
            #         rate_flag = True
            #         break

            return render(request,'movieDetail.html',{
                'movie_rating':movie_rating,
                'update':update,
                'rate_flag':rate_flag
            })
        except Movie.DoesNotExist:
            return redirect('core:profile_list')

    def get(self,request,profile_id,movie_id,*args, **kwargs):
        try:

            profile=Profile.objects.get(uuid=profile_id)
            movie=Movie.objects.get(id=movie_id)
            if profile.age_limit == 'Kids':
                movies=Movie.objects.exclude(id=movie_id).filter(adult=False).order_by('-vote_count')
            else:
                movies=Movie.objects.exclude(id=movie_id).order_by('-vote_count')

            query = request.GET.get('q')

            if query:
                query_list = movies.filter(Q(title__icontains=query)).distinct()
                return render(request, 'searchList.html', {
                    'movies': query_list,
                    'search_query':query,
                    'profile':profile
                })
            temp = list(MyList.objects.all().values().filter(movie_id=movie_id,profile=profile))

            if temp:
                update = temp[0]['watch']
            else:
                update = False
            mo={}
            directorl = movies.filter(director=movie.director)
            # castl=movie.cast.split(',')
            # for cast in castl:
            #     mo[cast]=
            genresl=movie.genre
            for genres in genresl:
                mo[genres]=sorted(movies, key=lambda a: genres in a.genre, reverse=True)[0:7]

            return render(request,'movieDetail.html',{
                'movie':movie,
                'directorlist':directorl,
                'movies':mo,
                'profile':profile,
                'update':update
            })
        except Movie.DoesNotExist:
            return redirect('core:profile_list')

@method_decorator(login_required,name='dispatch')
class ShowMovie(View):
    def get(self,request,movie_id,*args, **kwargs):
        try:
            
            movie=Movie.objects.get(id=movie_id)

            movie=movie.title.values()
            

            return render(request,'showMovie.html',{
                'movie':list(movie)
            })
        except Movie.DoesNotExist:
            return redirect('core:profile_list')

# To get similar movies based on user rating
def get_similar(movie_name,rating,corrMatrix):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

# Recommendation Algorithm
def recommend(profile_id):
    profile=Profile.objects.get(uuid=profile_id)
    movie_rating=pd.DataFrame(list(MyRating.objects.all().values()))

    # new_user=movie_rating.profile_id.unique().shape[0]
    # current_user_id= profile_id
	# if new user not rated any movie
    # if current_user_id>new_user:
    #     movie=Movie.objects.get(id=19)
    #     q=MyRating(user=request.user,movie=movie,rating=0)
    #     q.save()

    if MyRating.objects.all().values().filter(profile=profile):

        userRatings = movie_rating.pivot_table(index=['id','profile_id'],columns=['movie_id'],values='rating')
        userRatings = userRatings.fillna(0,axis=1)
        corrMatrix = userRatings.corr(method='pearson')

        user = pd.DataFrame(list(MyRating.objects.filter(profile=profile).values())).drop(['profile_id','id'],axis=1)
        user_filtered = [tuple(x) for x in user.values]
        movie_id_watched = [each[0] for each in user_filtered]

        similar_movies = pd.DataFrame()
        for movie,rating in user_filtered:
            similar_movies = similar_movies.append(get_similar(movie,rating,corrMatrix),ignore_index = True)

        movies_id = list(similar_movies.sum().sort_values(ascending=False).index)
        movies_id_recommend = [each for each in movies_id if each not in movie_id_watched]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movies_id_recommend)])
        if profile.age_limit == 'Kids':
            movie_list=list(Movie.objects.filter(adult=False).filter(id__in = movies_id_recommend).order_by(preserved))
        else:
            movie_list=list(Movie.objects.filter(id__in = movies_id_recommend).order_by(preserved))
        return movie_list

@method_decorator(login_required,name='dispatch')
class Recommender(View):
    def get(self,request,profile_id):
        try:
            profile=Profile.objects.get(uuid=profile_id)
            if profile.age_limit == 'Kids':
                movies=Movie.objects.filter(adult=False).order_by('-vote_count')
            else:
                movies=Movie.objects.order_by('-vote_count')              
            
            query = request.GET.get('q')

            if query:
                query_list = movies.filter(Q(title__icontains=query)).distinct()
                return render(request, 'searchList.html', {
                    'movies': query_list,
                    'search_query':query,
                    'profile':profile
                })
            movie_list=recommend(profile_id)
            
            return render(request,'recommendation.html',{
            'movies':movie_list,
            'profile':profile
            })
        except Profile.DoesNotExist:
            return redirect(to='core:profile_list')

@method_decorator(login_required,name='dispatch')
class My_list(View):
    def get(self,request,profile_id):
        try:
            profile=Profile.objects.get(uuid=profile_id)
            if profile.age_limit == 'Kids':
                movies=Movie.objects.filter(adult=False).order_by('-vote_count')
            else:
                movies=Movie.objects.order_by('-vote_count')              
            
            query = request.GET.get('q')

            if query:
                query_list = movies.filter(Q(title__icontains=query)).distinct()
                return render(request, 'searchList.html', {
                    'movies': query_list,
                    'search_query':query,
                    'profile':profile
                })
            mylist=MyList.objects.all().filter(profile=profile,watch=True).values('movie_id')
            mymovieslist=Movie.objects.filter(id__in=mylist.values_list('movie_id'))
            
            return render(request,'mylist.html',{
            'movies':mymovieslist,
            'profile':profile
            })
        except Profile.DoesNotExist:
            return redirect(to='core:profile_list')
