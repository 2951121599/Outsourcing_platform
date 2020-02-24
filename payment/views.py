import copy
import json
# AliPay 2.0 版本演示demo
# 请用 pip3 freeze|grep -i 'sdk' 对比环境中库版本
from alipay import AliPay
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.conf import settings

app_private_key_string = open(settings.ALIPAY_KEY_DIRS + 'app_private_key.pem').read()
alipay_public_key_string = open(settings.ALIPAY_KEY_DIRS + 'alipay_publick_key.pem').read()

ORDER_STATUS = 1  # 1 待付款 2 已付款


class JumpView(View):
    def get(self, request):
        # 生成支付页面
        return render(request, 'payment/pay.html')

    def post(self, request):
        # 获取支付宝支付链接
        data = request.body
        json_obj = json.loads(data)
        order_id = json_obj.get('order_id')
        print('----order is ----')
        print(order_id)
        # TODO 该订单号需要后端查数据库校验
        # 初始化Alipay

        alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type='RSA2',
            debug=True
        )
        # 生成查询字符串
        # out_trade_no 订单号
        # total_amount  订单总价
        # subject 订单标题
        # return_url  用户支付完毕，支付宝给用户跳转至商户页面 GET；返回时支付宝提供了支付相关参数
        # notify_url  用户支付完毕后，支付宝将最终结果以POST形式 发至 商户 后端； 上线请将此地址更换为公网 ip
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=20,
            subject=order_id,
            return_url="http://127.0.0.1:8000/payment/result",
            notify_url="http://127.0.0.1:8000/payment/result"
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string

        return JsonResponse({'code': 200, 'pay_url': pay_url})


class ResultView(View):

    def get_verify(self, request_data):
        # 深拷贝 字典类参数
        data = copy.deepcopy(request_data)
        sign = data.pop('sign')
        # 校验 支付宝传回来的数据
        alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type='RSA2',
            debug=True
        )
        # data是支付宝传回来的数据-字典
        # sign是 支付宝传回来的签名
        # 此次验签只能证明  当前数据是支付宝返回；至于支付是否成功return url 和 notify url 有各自的校验方案
        is_verify = alipay.verify(data, sign)
        print('is_verify:*********************', is_verify)
        return data, is_verify, alipay

    def get(self, request):
        # return url 会请求此方法
        request_data = {k: request.GET[k] for k in request.GET.keys()}
        print('request_data:', request_data)
        data, is_verify, alipay = self.get_verify(request_data)
        print('data:', data)
        print('is_verify:', is_verify)
        print('alipay:', alipay)
        if is_verify is True:
            # 数据来源可靠 【支付宝】
            order_id = data.get('out_trade_no')
            # 根据order_id查询数据库 校验电商订单状态
            if ORDER_STATUS == 2:
                # 证明 notify url 已经改变了订单状态
                return HttpResponse('订单支付成功')
            else:
                # 商家主动询问一下支付宝，该订单 是否已经完成
                result = alipay.api_alipay_trade_query(out_trade_no=order_id)
                print('----主动查询结果----')
                print(result)
                if result.get('trade_status') == 'TRADE_SUCCESS':
                    # 更改订单状态
                    # ORDER_STATUS = 2
                    return HttpResponse('主动查询 订单已经成功支付')

                else:
                    return HttpResponse('支付未完成')

        else:
            # 违法访问
            return HttpResponse('!!!!')

    def post(self, request):
        # notify url  会请求此方法 支付结束后，支付宝第一时间 请求 notify url 并将 具体支付结果用表单形式提交
        request_data = {k: request.POST[k] for k in request.POST.keys()}
        data, verify, alipay = self.get_verify(request_data)
        if verify is True:
            # 验签成功 数据来源可靠【支付宝】
            # notify url 会比 return url多出 trade_status参数，此参数标明订单支付最终结果
            trade_status = data.get('trade_status')
            if trade_status == 'TRADE_SUCCESS':
                # 订单支付成功
                # 更改电商订单状态
                # ORDER_STATUS = 2
                return HttpResponse('success')
            else:
                return HttpResponse('trade failed')
        else:
            # 违法请求
            return HttpResponse('!!!!!!!')
