from django.contrib import admin

from .models import CarMake, CarModel


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of empty forms to display


# CarMakeAdmin class with CarModelInline
@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "country", "founded_year"]
    search_fields = ["name"]
    inlines = [CarModelInline]  # Add inline to show related CarModels


# CarModelAdmin class
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ["name", "car_make", "type", "year", "dealer_id"]
    list_filter = ["type", "year", "car_make"]
    search_fields = ["name", "car_make__name"]
