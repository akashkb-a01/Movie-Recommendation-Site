from django.contrib import admin
from .models import CustomUser,Profile,Movie,MyRating,MyList

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Movie
from django import forms
from .models import Movie
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('adult','budget','genre','id','imdb_id','original_language','original_title','overview','popularity','poster_path','release_date','revenue','runtime','tagline','title','vote_average','vote_count','year','cast','keywords','director')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            
            file_data = pd.read_csv(csv_file)

            for x in range(file_data.shape[0]):
                created = Movie.objects.update_or_create(
                    adult = file_data['adult'][x],
                    budget = file_data['budget'][x],
                    genre = file_data['genre'][x],
                    id = file_data['id'][x],
                    imdb_id = file_data['imdb_id'][x],
                    original_language = file_data['original_language'][x],
                    original_title = file_data['original_title'][x],
                    overview = file_data['overview'][x],
                    popularity = file_data['popularity'][x],
                    poster_path = file_data['poster_path'][x],
                    release_date = file_data['release_date'][x],
                    revenue = file_data['revenue'][x],
                    runtime = file_data['runtime'][x],
                    tagline = file_data['tagline'][x],
                    title = file_data['title'][x],
                    vote_average = file_data['vote_average'][x],
                    vote_count = file_data['vote_count'][x],
                    year = file_data['year'][x],
                    cast = file_data['cast'][x],
                    keywords = file_data['keywords'][x],
                    director = file_data['director'][x]
                    )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

admin.site.register(Movie, CustomerAdmin)


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(MyList)
admin.site.register(MyRating)
