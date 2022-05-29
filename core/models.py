from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField
import uuid

AGE_CHOICES=(
    ('All','True'),
    ('Kids','False')
)

GENRES=(
    ('Action','Action'),
    ('Adventure','Adventure'),
    ('Adult','Adult'),
    ('Animation','Animation'),
    ('Biography','Biography'),
    ('Comedy','Comedy'),
    ('Crime','Crime'),
    ('Documentary','Documentary'),
    ('Drama','Drama'),
    ('Family','Family'),
    ('Fantasy','Fantasy'),
    ('History','History'),
    ('Horror','Horror'),
    ('Music','Music'),
    ('Musical','Musical'),
    ('Mystery','Mystery'),
    ('Romance','Romance'),
    ('Sci-Fi','Sci-Fi'),
    ('Short','Short'),
    ('Sport','Sport'),
    ('Thriller','Thriller'),
    ('War','War'),
    ('Western','Western')
)

MOVIE_TYPE=(
    ('single','Single'),
    ('seasonal','Seasonal')
)

class CustomUser(AbstractUser):
    profiles=models.ManyToManyField('Profile')


class Profile(models.Model):
    name=models.CharField(max_length=225)
    age_limit=models.CharField(max_length=5,choices=AGE_CHOICES)
    uuid=models.UUIDField(default=uuid.uuid4,unique=True)


    def __str__(self):
        return self.name +" "+self.age_limit

class Movie(models.Model):
    adult=models.BooleanField(null=True)
    budget=models.IntegerField(null=True)
    genre=MultiSelectField(choices=GENRES,max_choices=5,blank=True)
    id=models.IntegerField(unique=True,primary_key=True)
    imdb_id=models.CharField(max_length=20,blank=True)
    original_language=models.CharField(max_length=2,null=True)
    original_title=models.CharField(max_length=50,null=True)
    overview:str=models.TextField(blank=True)
    popularity=models.DecimalField(decimal_places=6,max_digits=9,null=True)
    poster_path= models.CharField(max_length=100,blank=True,null=True)
    release_date=models.DateField(default=datetime.today)
    revenue=models.IntegerField(null=True)
    runtime=models.IntegerField(null=True)
    tagline=models.TextField(blank=True)
    title:str=models.CharField(max_length=225)
    vote_average=models.DecimalField(decimal_places=1,max_digits=3,null=True)
    vote_count=models.IntegerField(null=True,default=0)
    year=models.IntegerField(null=True)
    cast=models.CharField(max_length=255,null=True)
    keywords=models.CharField(max_length=255,null=True)
    director=models.CharField(max_length=30,null=True)
    created=models.DateTimeField(auto_now_add=True)
    
class MyRating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

class MyList(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch = models.BooleanField(default=False)
