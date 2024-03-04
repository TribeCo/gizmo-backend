from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart
from ..serializers import *
from ..models import User
from config.settings import SMS_PASSWORD,SMS_USERNAME
import random
from rest_framework.permissions import IsAuthenticated
#---------------------------
"""
    The codes related to the site's user model are in this app.
    api's in user_apies.py:

    1- CheckPhoneNumberAPIView --> This API checks whether the phone number is in the database or not
    2- CreateUserWithPhoneNumberAPIView --> Create user with phone number
    3- CheckCodeAPIView --> Check the code user entered and code is in database
    4- UpdateSignUpAPIView --> Sign up for frontend
    5- PasswordChangeRequest --> Password change request
    6- ChangePassword --> It change user password if can_change_password is active.
    

"""
#---------------------------
messages_for_front = {
    'user_created' : 'کاربر جدید ایجاد شد.',
    'user_not_found' : 'کاربر یافت نشد',
    'article_not_found' : 'مقاله یافت نشد',
    'product_not_found' : 'محصول یافت نشد',
    'comment_not_found' : 'نظر یافت نشد',
    'comment_deleted' : 'نظر حذف شد',
    'user_found' : 'کاربر یافت شد.',
    'password_changed' : 'رمز عبور با موفقیت تغییر کرد.',
    'wrong_coode' : 'کد اعتبارسنجی نامعتبر است.',
    'not_access' : 'شما دسترسی لازمه را ندارید.',
    'not_match': 'رمز های عبور یکسان نیستند.',
    'right_code' : 'کد اعتبارسنجی صحیح است.',
    'code_sent' : 'کد ارسال شد.',
    'favorite_products_not_found': 'محصول مورد علاقه ای وجود ندارد',
    'product_added_to_wishlist': 'محصول به لیست مورد علاقه‌ها اضافه شد',
    'product_removed_from_wishlist': 'محصول از لیست مورد علاقه‌ها حذف شد',
    
}
#---------------------------
class CheckPhoneNumberAPIView(APIView):
    """This API checks whether the phone number is in the database or not"""
    def get(self, request,phone_number):
        try:
            user = User.objects.get(phoneNumber=phone_number)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found'],'in_database':'fasle'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': messages_for_front['user_found'],'in_database':'true'}, status=status.HTTP_200_OK)
#---------------------------
class CreateUserWithPhoneNumberAPIView(APIView):
    """Create user with phone number"""
    def post(self, request):
        text_sms = "name عزیز به گیزموشاپ خوش آمدید.\nکد احرازسنجی شما: code"
        link_sms = f"https://www.0098sms.com/sendsmslink.aspx?FROM=50002220096&TO=PhoneNumberUser&TEXT=TextCode&USERNAME={SMS_USERNAME}&PASSWORD={SMS_PASSWORD}&DOMAIN=0098"
        
        
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():      
            user = User(
                phoneNumber = serializer.validated_data['phoneNumber'],
                email = f"{serializer.validated_data['phoneNumber']}@gmail.com",
            )

            user.save()

            user.is_active = False
            code = random.randint(10000, 99999)
            user.code = code

            cart = Cart(user = user)
            cart.save()
            user.cart = cart

            user.save()

            # send code to user
            # text_sms = text_sms.replace("name" ,user.full_name)
            text_sms = text_sms.replace("code" , str(user.code))

            send_sms = link_sms.replace("PhoneNumberUser",user.phoneNumber)
            send_sms = send_sms.replace("TextCode",text_sms)

            # response = requests.get(send_sms)

            response_data = {
                'phoneNumber' : user.phoneNumber,
                'id' : user.id
            }
            

            return Response({'data' : response_data}, status=status.HTTP_201_CREATED)

            # if response.status_code == 200:
            #     return Response({'data' : response_data,'response_sms': response.json()}, status=status.HTTP_201_CREATED)
            # else:
            #     print('درخواست با خطا مواجه شد:', response.status_code)

            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CheckCodeAPIView(APIView):
    """Check the code user entered and code is in database"""
    def post(self, request):

        code = request.data['code']
        phoneNumber = request.data['phoneNumber']

        if(not phoneNumber):
            return Response({'message': "users must have phoneNumber"}, status=status.HTTP_400_BAD_REQUEST)
        
        if(not code):
            return Response({'message': "users must have code"}, status=status.HTTP_400_BAD_REQUEST)

        try :
            user = User.objects.get(phoneNumber = phoneNumber)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_400_BAD_REQUEST)

        if(str(user.code) == str(code)):
            return Response({'message' : 'code is valid.'}, status=status.HTTP_200_OK)
        return Response({'message' : 'code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

#---------------------------
class UpdateSignUpAPIView(APIView):
    """Sign up for frontend"""
    def post(self, request):

        phoneNumber = request.data['phoneNumber']
        email = request.data['email']
        full_name = request.data['full_name']
        password = request.data['password']


        if(not phoneNumber):
            return Response({'message': "users must have phoneNumber"}, status=status.HTTP_400_BAD_REQUEST)
        
        if(not email):
            return Response({'message': "users must have email"}, status=status.HTTP_400_BAD_REQUEST)
        
        if(not full_name):
            return Response({'message': "users must have full name"}, status=status.HTTP_400_BAD_REQUEST)

        if(not password):
            return Response({'message': "users must have password"}, status=status.HTTP_400_BAD_REQUEST)

        try :
            user = User.objects.get(email = email)
            return Response({'message': "use another email"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        
        try :
            user = User.objects.get(phoneNumber = phoneNumber)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_400_BAD_REQUEST)

        if(user.is_active):
            return Response({'message': "can not update"}, status=status.HTTP_400_BAD_REQUEST)

        
        user.full_name = full_name
        user.email = email
        user.set_password(password)
        user.is_active = True
        code = random.randint(10000, 99999)
        user.code = code

        user.save()


        response_data = {
            'phoneNumber' : user.phoneNumber,
            'full_name' : user.full_name,
            'id' : user.id
        }       

        return Response({'data' : response_data}, status=status.HTTP_200_OK)
            
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class PasswordChangeRequest(APIView):
    def post(self, request):
        """
            Password change request
            urls : domain.com/..../users/update/password/
            Sample json :
            {
            "phoneNumber" : "09303615324",
            }

        """

        info = PasswordChangeRequestSerializer(data=request.data)
        

        if info.is_valid():
            try :
                user = User.objects.get(phoneNumber = info.validated_data['phoneNumber'])
            except User.DoesNotExist:
                return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_400_BAD_REQUEST)

            user.can_change_password = True
            code = random.randint(10000, 99999)
            user.code = code
            user.save()

            # send Code to User
            
            return Response({'message': messages_for_front['code_sent']}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ChangePassword(APIView):
    """
            It change user password if can_change_password is active.
            urls : domain.com/..../users/change/password/
            Sample json :
            {
            "phoneNumber" : "09345454678",
            "password" : "338dsfs3fsaengh7",
            "code" : 76766
            }

    """
    def post(self, request):
        info = PasswordChangeSerializer(data=request.data)    

        if info.is_valid():
            try :
                user = User.objects.get(phoneNumber = info.validated_data['phoneNumber'])
            except User.DoesNotExist:
                return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_400_BAD_REQUEST)
            if (user.can_change_password):
                if(str(user.code) == str(info.validated_data['code'])):

                    user.set_password(info.validated_data.get('password'))
                    user.can_change_password = False
                    user.code = random.randint(10000, 99999)
                    user.save()

                    return Response({'message': messages_for_front['password_changed']}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': messages_for_front['wrong_coode']}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class OldChangePassword(APIView):
    """
            It change user old password.
            urls : domain.com/..../users/change/password/old/
            Sample json :
            {
                "phoneNumber": "09345454678",
                "new_password": "sdfmkwefjoiwejf",
                "new_password_confirm": "sdfmkwefjoiwejf",
                "password": "338dsfs3fsaengh7"
            }

    """
    def post(self, request):
        info = OldPasswordChangeSerializer(data=request.data)    

        if info.is_valid():
            try :
                user = User.objects.get(phoneNumber = info.validated_data['phoneNumber'])
            except User.DoesNotExist:
                return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_400_BAD_REQUEST)
            
            if (user.check_password(str(info.validated_data['password']))):
                if((user == request.user) and (info.validated_data['new_password_confirm'] == info.validated_data['new_password'])):

                    user.set_password(info.validated_data.get('new_password'))
                    user.can_change_password = False
                    user.code = random.randint(10000, 99999)
                    user.save()

                    return Response({'message': messages_for_front['password_changed']}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': messages_for_front['not_match']}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message': messages_for_front['not_access']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
