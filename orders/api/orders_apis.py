from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from ..serializers import *
from ..models import Order, OrderItem
from accounts.models import DeliveryInfo,Payments
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from config.settings import merchant
import requests
import json
#---------------------------
"""
    The codes related to the site's orders are in this app.
    api's in api_views.py :

    1- CreateOrderAPIView --> Creats an order with post method
    2- ReadOrderAPIView -->  Gets a single order 
    3- ListOrdersAPIView --> Lists all of the orders
    4- DeleteOrderAPIView --> Delets an order with id 
    5- SetOrderItemsQuantityAPIView --> Sets the amount of one single product
    6- ListOrderItemsAPIview --> Lists all items of one order
    7- DeleteProductToOrderAPIView --> Removes a product from the order
    8- ConvertCartToOrderAPIView --> converts an instance of a Cart model to an instance of an Order model

"""
#---------------------------
message_for_front = {
    'order_created': 'سفارش ثبت شد',
    'order_not_found': 'سفارش یافت نشد.',
    'order_item_not_found': 'آیتم سفارش یافت نشد',
    'order_updated': 'سفارش با موفقیت آپدیت شد.',
    'no_cart_items_in_user_cart': 'سبد کاربر خالی می باشد',
    'cart_converted_to_order': 'سفارشات ثبت شدند',
    "not_order" : 'جنین سفارشی در دیتابیس وجود ندارد.',
    "not_connected" : ' اتصال به درگاه ناموفق بود.',
    "too_long" : 'زمان بیش حد سپری شده برای اتصال به درگاه.',
    "not_success_connect" : 'اتصال ناموفق.',
    "success" : 'پرداخت با موفقیت انجام شد.',
    "payed" : 'پرداخت انجام شده بوده است.',
    "not_upload" : 'آپلود با مشکل مواجه شد.',
    "success_upload" : "آپلود با موفقیت انجام شد. برای پیگیری سفارش به داشبورد مراجعه کنید.",
    "user_not_match" : "این کاربر دسترسی لازم ندارد"
}
#---------------------------
if True:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

MERCHANT = merchant
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
# amount = 11000  # Rial / Required
description = "گیزموشاپ"  # Required
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:3000/success'
#---------------------------
class CreateOrderAPIView(APIView):
    """
        creats an order object.
        login is required.        
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        serializer = OrderSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({'message': message_for_front['order_created']}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadOrderAPIView(generics.RetrieveAPIView):
    """reads a single order object with ID(domain/.../ID/)"""
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#---------------------------
class ListOrdersAPIView(generics.ListAPIView):
    """read all of the order objects"""
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#---------------------------
class DeleteOrderAPIView(generics.DestroyAPIView):
    """deletes a single order object with ID(domain/.../ID/)"""
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#---------------------------
class SetOrderItemsQuantityAPIView(APIView):
    """
    set the quantity of a item in order.
    login is required.
    required fields{
        order_id
        item_id
        quantity
    }
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        order_id = request.data.get('order_id')
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        
        try:
            order = user.orders.get(id = order_id)
        except:
            return Response({'message':message_for_front['order_not_found']},status.HTTP_404_NOT_FOUND)
        
        try:
            item = order.items.get(id = item_id)
        except:
            return Response({'message':message_for_front['order_item_not_found']},status.HTTP_404_NOT_FOUND)
        
        item.quantity = quantity
        item.save()

        return Response({'message':message_for_front['order_updated']},status=status.HTTP_200_OK)
#---------------------------
class ListOrderItemsAPIview(APIView):
    """Lists all items of an order with order_ID(domaim/.../ID/)"""
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):
        try:
            order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            return Response({'message':message_for_front['order_not_found']},status.HTTP_404_NOT_FOUND)
        
        serializer = OrderItemsSerializer(order.items, many=True)

        return Response({'data': serializer.data})
#---------------------------
class DeleteProductToOrderAPIView(APIView):
    """Remove a product from the order with ID(domain/.../ID/)"""
    permission_classes = [IsAuthenticated]
    def delete(self, request,pk):
        try:
            item = OrderItem.objects.get(id=pk)
        except OrderItem.DoesNotExist:
            return Response({'message':message_for_front['order_item_not_found']}, status=status.HTTP_404_NOT_FOUND)    

        item.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT) 
#---------------------------
class PayMoneyAPIView(APIView):
    """
        Create a link for redirecting user to portal bank.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        amount = user.total_price() 

        data = {
            "MerchantID": "007b7418-afdb-47ff-85fc-3719884056ef",
            "Amount": amount,
            "Description": description,
            "Phone": user.phoneNumber,
            # change this url
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)

        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

            response_dict = json.loads(response.text)
            status = response_dict['Status']
            authority = response_dict['Authority']

            print(response_dict)


            if(status == 100):
                redirect_url = f"{ZP_API_STARTPAY}{authority}"
                pay_obj = Payments(authority = authority,
                    user = user,
                    amount = amount
                    )

                pay_obj.save()
                return Response({'redirect_url':redirect_url,})
                
            
            return Response({'message':message_for_front['not_connected'],})


        
        except requests.exceptions.Timeout:
            return Response({'message':message_for_front['too_long'],})
        except requests.exceptions.ConnectionError:
            return Response({'message':message_for_front['not_success_connect'],})
#---------------------------
class VerifyAPIView(APIView):
    """
        This api checks whether the payment has been made correctly or not.
        converts a cart to order.
        login required. 
    """
    def post(self, request):
        t_status = request.POST.get('status')
        t_authority = request.POST.get('authority')


        try:
            pay_obj = Payments.objects.get(authority=t_authority)
        except Payments.DoesNotExist:
            return Response({'message':message_for_front['not_order'],})

        user = pay_obj.user
        amount = user.total_price()

        
        if(t_status == "NOK"):
            return Response({'message':message_for_front['not_success_connect'],})
        
        elif(t_status == "OK"):
            data = {
                "MerchantID": MERCHANT,
                "Amount": amount,
                "Authority": t_authority,
            }
        
            data = json.dumps(data)
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

            response_dict = json.loads(response.text)
            status = response_dict['Status']
            RefID = response_dict['RefID']

            if status == 100 or status == 101:
                    pay_obj.ref_id = RefID
                    pay_obj.save()

                    cart = user.cart

                    try:
                        cart_items = cart.items.all()
                    except:
                        return Response({'message': message_for_front['no_cart_items_in_user_cart']}, status=status.HTTP_404_NOT_FOUND)
                    
                    order = Order(user = user,address=user.addresses.get(current=True),paid=True)    
                    order.save()    

                    for item in cart_items:
                        item.product.update_warehouse(item.color.id,item.quantity)
                        order_item = OrderItem(product= item.product,
                        price= item.price,quantity= item.quantity,color= item.color,
                        order= order)
                        order_item.save()

                        order.items.add(order_item)

                    order.delivery_info = user.delivery_info
                    user.delivery_info = None
                    user.save()

                    if(cart.coupon):
                        order.discount = cart.coupon.discount

                    order.authority = t_authority
                    order.ref_id = RefID
                    order.save()

                    for item in cart_items:
                        item.delete()

                    info = OrderSerializerForCart(order)
                                
                    return Response({'message':message_for_front['success'],'data':info.data})

            else:
                return Response({'message':message_for_front['not_success_connect'],})
        else:
            return Response({'message':message_for_front['not_success_connect'],})
#---------------------------
class FactorAPIView(APIView):
    """
        This api give front exepcted data for factor.
    """
    permission_classes = [IsAuthenticated]
    def get(self , request,pk):
        try:
            order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            return Response({'message':message_for_front['order_not_found']},status.HTTP_404_NOT_FOUND)
        
        if order.user != request.user :
            return Response({'message':message_for_front['user_not_match']},status.HTTP_400_BAD_REQUEST)

        serialized_order = OrderSerializer(order)

        return Response({'data': serialized_order.data})

        
#---------------------------
from django.template.loader import get_template
from django.http import HttpResponse

def generate_pdf(request):
    template = get_template('orders/factor.html')
    info = {}
    order = Order.objects.get(id=7)
    info['order'] = order
    rendered_html = template.render({'data': info})

    # return HttpResponse(rendered_html)
    return render(request,'orders/factor.html',info)
#---------------------------

