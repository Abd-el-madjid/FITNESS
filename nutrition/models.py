from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.conf import settings
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Club(models.Model):
    CLUB_TYPE_CHOICES = [
        ('Football', 'Football'),
        ('Handball', 'Handball'),
        ('Basketball', 'Basketball'),
        # Add more choices as needed
    ]

    club_name = models.CharField(max_length=100)
    club_type = models.CharField(max_length=50, choices=CLUB_TYPE_CHOICES)
    logo = models.ImageField(upload_to='club_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.club_name


class Person(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=[(
        'M', 'Male'), ('F', 'Female'), ('O', 'Other')])

    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - \
            ((today.month, today.day) <
             (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def __str__(self):
        return self.name


class Player(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    height = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return self.person.name


class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)
    proteins = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Diet(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goal_weight = models.DecimalField(max_digits=5, decimal_places=1)
    calorie_intake = models.IntegerField()
    activity_lvl = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diet for {self.player.person.name}"


class NutritionalInfo(models.Model):
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE)
    protein_g = models.DecimalField(max_digits=5, decimal_places=1)
    carb_g = models.DecimalField(
        max_digits=5, decimal_places=1, default=0)  # Specify a default value
    fat_g = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return f"Nutritional info for {self.diet}"



class Meal(models.Model):
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category} for {self.diet.player.person.name}'s diet"


class FoodChoice(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.food_item} for {self.meal}"
    
    
    

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    calories_burned_per_hour = models.IntegerField()

    def __str__(self):
        return self.name


class PlayerExercise(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    duration = models.IntegerField()  # Duration in minutes
    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.person.name} performed {self.exercise.name} for {self.duration} minutes"




