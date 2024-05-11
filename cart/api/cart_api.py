from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CartItem,Cart
from ..serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
#---------------------------
"""
    The codes related to the site's cart are in this app.
    api's in cart_api.py :

    1- CartDetailAPIView --> Getting the user's shopping cart information
    2- AddProductToCartAPIView --> Add a product to the cart
    3- DeleteProductToCartAPIView --> Remove a product from the cart
    4- CartItemUpdateView --> Update Cart item information with ID

    5- ClearCartAPIView --> Clear the entire shopping cart
"""
#---------------------------
messages_for_front = {
    'item_not_found' : 'محصول یافت نشد.',
    'delete_product' : 'محصول از سبد خخرید حذف شد',
    'add_product' : 'محصول با موفقیت به سبد خرید اضافه شد.',
    'update_product' : 'محصول آپدیت شد.',
    'cart_cleared' : 'سبد خرید خالی شد.',
    'not_availble_product' : 'محصول مورد نظر موجود نمی باشد',
    'not_enough_product' : 'محصول به تعداد کافی موجود نمی باشد.',
}
#---------------------------
class CartDetailAPIView(APIView):
    """Getting the user's shopping cart information"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = CartSerializer(request.user.cart)
        return Response({'cart':serializer.data}, status=status.HTTP_200_OK)
#---------------------------
class CartDetailLocalAPIView(APIView):
    """Getting the user's shopping cart information"""
    serializer_class = CartLocalSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = CartLocalSerializer(request.user.cart)
        return Response({'cart':serializer.data}, status=status.HTTP_200_OK)
#---------------------------
class AddProductToCartAPIView(APIView):
    """
        Add a product to the cart
        {
            "quantity": 1,
            "color": 3, --> color id
            "product": 6 --> product id
        }  
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    def post(self, request,):
        serializer = CartItemSerializer(data=request.data)

        try:
            cart = request.user.cart
        except :
            user = request.user
            cart = Cart(user = user)
            cart.save()
            user.cart = cart
            user.save()

        if serializer.is_valid():
            product = serializer.validated_data['product']
            color = serializer.validated_data['color']
            quantity = serializer.validated_data['quantity']
            if(product.is_available):
                product_color_object = product.product_color.get(color__id=color.id)
                if(product_color_object.quantity >= quantity):
                    item = serializer.save(cart=cart,price=0)
                    item.price = item.product.discounted_price_int
                    item.save()
                else:
                    return Response({'message':messages_for_front['not_enough_product']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':messages_for_front['not_availble_product']}, status=status.HTTP_400_BAD_REQUEST)
            data_r = CartItemSerializer(item)
            return Response({'message':messages_for_front['add_product'],'data':data_r.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
#---------------------------
class AddListOfProductsToCartAPIView(APIView):
    """
        Add a list of products to the cart
        [
            {
                "quantity": 1,
                "color": 3, --> color id
                "product": 6 --> product id
            },
            {
                "quantity": 2,
                "color": 1, --> color id
                "product": 11 --> product id
            }
        ]  
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def post(self, request):
        data = request.data
        serializer_list = []

        try:
            cart = request.user.cart
        except Cart.DoesNotExist:
            user = request.user
            cart = Cart(user=user)
            cart.save()
            user.cart = cart
            user.save()

        for item_data in data:
            serializer = CartItemSerializer(data=item_data)
            if serializer.is_valid():
                product = serializer.validated_data['product']
                color = serializer.validated_data['color']
                quantity = serializer.validated_data['quantity']

                if product.is_available:
                    product_color_object = product.product_color.get(color__id=color.id)
                    if product_color_object.quantity >= quantity:
                        item = serializer.save(cart=cart, price=0)
                        item.price = item.product.discounted_price_int
                        item.save()
                    else:
                        return Response({'message': messages_for_front['not_enough_product']}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': messages_for_front['not_enough_product']}, status=status.HTTP_400_BAD_REQUEST)

                serializer_list.append(serializer)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = CartSerializer(request.user.cart)
        return Response({'message': messages_for_front['add_product'],'data':serializer.data}, status=status.HTTP_201_CREATED)

#---------------------------
class DeleteProductToCartAPIView(APIView):
    """Remove a product from the cart"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def delete(self, request,pk):
        try:
            item = CartItem.objects.get(id=pk)
        except CartItem.DoesNotExist:
            return Response({'message':messages_for_front['item_not_found']}, status=status.HTTP_404_NOT_FOUND)    

        item.delete()
        return Response({'message':messages_for_front['delete_product']}, status=status.HTTP_204_NO_CONTENT) 
#---------------------------
class CartItemUpdateView(APIView):
    """Update Cart item information with ID"""
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request,pk):
        try:
            item = CartItem.objects.get(id=pk)
        except CartItem.DoesNotExist:
            return Response({'message':messages_for_front['item_not_found']}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemUpdateSerializer(data=request.data,instance=item)
        
        if serializer.is_valid():
            serializer.save(product=item.product)
            return Response({'message':messages_for_front['update_product'],'item':serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
#---------------------------
class ClearCartAPIView(APIView):
    """Clear the entire shopping cart"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart = request.user.cart

        for item in cart.items.all():
            item.delete()

        return Response({'message':messages_for_front['cart_cleared']}, status=status.HTTP_204_NO_CONTENT) 
#---------------------------
class UnknownCartAPIView(APIView):
    """
        Ceate cart for front-end.
        [
            {
                "quantity": 1,
                "color": 3, --> color id
                "product": 6 --> product id
            },
            {
                "quantity": 2,
                "color": 1, --> color id
                "product": 11 --> product id
            }
        ]  
    """
    serializer_class = CartItemSerializer

    def post(self, request):
        data = request.data
        serializer_list = []


        user = User.objects.get(phoneNumber="093012345")
        cart = user.cart

        for item_data in data:
            serializer = CartItemSerializer(data=item_data)
            if serializer.is_valid():
                product = serializer.validated_data['product']
                color = serializer.validated_data['color']
                quantity = serializer.validated_data['quantity']

                if product.is_available:
                    product_color_object = product.product_color.get(color__id=color.id)
                    if product_color_object.quantity >= quantity:
                        item = serializer.save(cart=cart, price=0)
                        item.price = item.product.discounted_price_int
                        item.save()
                    else:
                        return Response({'message': messages_for_front['not_enough_product']}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': messages_for_front['not_enough_product']}, status=status.HTTP_400_BAD_REQUEST)

                serializer_list.append(serializer)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = CartSerializer(cart)
        data_for_front = serializer.data
        cart_items = cart.items.all()
        for item in cart_items:
            item.delete()
        return Response({'message': messages_for_front['add_product'],'data':data_for_front}, status=status.HTTP_201_CREATED)
#---------------------------