import json

from django.shortcuts import render,get_object_or_404,redirect
from django.http import  JsonResponse
from django.views import View
from django.db.models import Count,Sum
from django.views.decorators.csrf import csrf_exempt
from uuid import UUID
from restaurant_management.models import Cart, Category,Food, FoodImage, Table

# Create your views here.
class HomePageView(View):
    
    def get(self,request,*args,**kwargs):
        table_id = self.kwargs.get("table_id")
        table_id = UUID(table_id)  # Convert string to UUID
        table = get_object_or_404(Table, table_unique_id=table_id)
        total_cart_items = Cart.objects.filter(table=table).aggregate(
            total=Sum("quantity")
        )["total"] or 0

                
        categories = Category.objects.annotate(
            food_count=Count('food_category')
        ).filter(food_count__gt=0)

        context = {
            "categories" : categories,
            "total_cart_items" : total_cart_items,
            "table_id" : table_id
        }
        
        return render(request,"home.html",context=context)
    


class ProductListFetchView(View):
    def get(self,request,*args,**kwargs):
        
        category=request.GET.get("category")
        foods = Food.objects.all()
        if category:
            foods = foods.filter(category=category)
        

        all_context = []
        for food in foods :
            context = {}
            context["images"] = []
            context["id"] = food.id
            context["name"] = food.name 
            context["price"] = food.price
            context["category_name"] = food.category.name if food.category else "Food"
            all_images = FoodImage.objects.filter(food=food)
            for image in all_images:
                context["images"].append(image.image.url)
            all_context.append(context)
        
        return JsonResponse(data=all_context,safe=False)



class CartView(View):
    
    def get(self,request,*args,**kwargs):
        table_id = self.kwargs.get("table_id")
        table_id = UUID(table_id)  # Convert string to UUID
        table = get_object_or_404(Table, table_unique_id=table_id)
                
        items  = Cart.objects.filter(table=table).order_by("-id")

        total_cart_items = Cart.objects.filter(table=table).aggregate(
            total=Sum("quantity")
        )["total"] or 0

        context = {
            "cart_items" : items,
            "table_id" : table_id,
         "total_cart_items" : total_cart_items,
        }

        
        return render(request,"cart.html",context=context)
    


class CartDeleteView(View):

    def get(self,request,*args,**kwargs):
        table_id = self.kwargs.get("table_id")
        cart_id = self.kwargs.get("cart_id")
        table_id = UUID(table_id)  # Convert string to UUID
        table = get_object_or_404(Table, table_unique_id=table_id)
        
        items  = Cart.objects.filter(table=table,id=cart_id)
        items.delete()
        return redirect("restaurant_management:cart",table_id=table_id)
    
class AddToCart(View):

    def post(self,request,*args,**kwargs):
        data = json.loads(request.body)
        table_id = self.kwargs.get("table_id")
        product_id= int(data.get("product_id"))
        quantity = int(data.get("quantity"))
        table_id = UUID(table_id)  # Convert string to UUID
        table = get_object_or_404(Table, table_unique_id=table_id)
        food = get_object_or_404(Food,id=product_id)
        cart ,created = Cart.objects.get_or_create(table=table,food=food)
        cart.quantity = quantity
        cart.save()
        return JsonResponse(data={"message":"added"},safe=False)
        
        
