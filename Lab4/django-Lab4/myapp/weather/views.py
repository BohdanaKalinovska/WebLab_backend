import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import AuthUserForm, RegisterUserForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def index(request):
    appid = ''
    #виводити температуру в цельсіях
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&lang=ua&units=metric&appid=' + appid
    #відправка даних по методу post (означає те що ми можемо отримати ці дані, записати ці дані в табличку
    #і за допомогою кнопки submit перезагрузити сторінку) і ми перевіряємо метод відправки
    err_msg = ''
    message = ''
    message_class = ''
    message_about_weather = ''
    if(request.method == 'POST'):
        form = CityForm(request.POST) #дані які отримали від користувача

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            #Перевідка на те чи не повторюється місто в пошуку
            if existing_city_count == 0:
                res = requests.get(url.format(new_city)).json()
                #Перевірка на існування введеного міста
                if res['cod'] == 200:
                    form.save() #зберігає дані в базу даних
                else:
                    err_msg = "City does not exist in the world!"
            else:
                err_msg = 'City already exists in the database!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
             message = 'City added successfully!'
             message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        res = requests.get(url.format(city)).json()
        factor = res["weather"][0]["main"]
        if factor=='Thunderstorm':
            message_about_weather = 'Синоптики обіцяють гарну погоду..но вперто не зізнаються де ...'
        elif factor=='Rain':
            message_about_weather = 'Пішов дощ. Але потім не витримав і побіг'
        elif factor=='Snow':
            message_about_weather = 'Якщо ви встали зранку і немає гарячої води і опалення, знайте - випав сніг !'
        elif factor=='Clear':
            message_about_weather = 'Парасолька - це спеціальний амулет від дощу. Коли вона з вами - дощу не буде!'
        elif factor=='Clouds':
            message_about_weather = 'Посміхнися, і всі хмари розійдуться від цієї наглості :)'
        elif factor=='Fog':
            message_about_weather = 'Немає туману, з якого не було б виходу. Головне - триматися і йти вперед.'
        elif factor=='Tornado':
            message_about_weather = 'Коротко про погоду: легкий бриз здуває лице з черепа.'
        else:
            message_about_weather = 'Про погоду: такого безглуздого перельоту на південь птахи ще не здійснювали.'
        print(factor)
        city_weather = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'pressure': res["main"]["pressure"],
            'humidity': res["main"]["humidity"],
            'wind': res["wind"]["speed"],
            'descript_1': res["weather"][0]["main"],
            'descript_2': res["weather"][0]["description"],
            'icon': res["weather"][0]["icon"],
            'message_about_weather': message_about_weather
        }
        weather_data.append(city_weather)
    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name = city_name).delete()
    return redirect('home')

class MyprojectLoginView(LoginView):
    template_name = "weather/login.html"
    form_class = AuthUserForm
    success_url = reverse_lazy('home')
    def get_success_url(self):
        return self.success_url

class RegisterUserView(CreateView):
    model = User
    template_name = "weather/register_page.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    success_msg = 'Користувач успішно створений'
    def form_valid(self,form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username = username, password = password)
        login(self.request, aut_user)
        return form_valid

class MyprojectLogout(LogoutView):
    next_page = reverse_lazy('home')
