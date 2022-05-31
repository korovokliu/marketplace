from django.shortcuts import get_object_or_404, render
from .models import Product
from order.models import OrderItem
from django.http import JsonResponse


def product_page(request, slug):
    if request.method == 'GET':
        product = get_object_or_404(Product, slug=slug)
        context = {"product": product}
        return render(request, 'product_page/product_page.html', context=context)
    if request.method == 'POST':
        product_id = request.POST.get('id')
        action_type = request.POST.get('action')
        try:
            order = OrderItem.objects.get_or_create(product_id=product_id)
            # Возвращает объект по типу (<OrderProduct: OrderProduct object (1)>, False)
            if action_type == 'add':
                order[0].quantity += 1
                order[0].save()
            elif action_type == 'delete':
                order[0].quantity -= 1
                order[0].save()
        except Exception as e:
            print(f"Ошибка: {e}")
            return JsonResponse({'status': 'error'})
        else:
            return JsonResponse({'status': 'ok', 'count': str(order[0].quantity)})