#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz

#加载模块
import sys
sys.path.append('..')
import json,prettytable,time,collections
from core import terminal_pay
#将json中的数据赋值为变量
user_info=json.load(open('../db/mall_user.json','r'))
goods=json.load(open('../db/goods.json','r'))
save_cart=json.load(open('../db/mall_cart.json','r'))
#设置时间戳的变量
time_now=time.strftime('%Y-%m-%d %H:%M:%S')
cart=None
user_name=None
balance=None

#打开用户锁定文件,并将其转化为列表
user_lock=open('../db/mall_user_lock','r+')
locker=user_lock.readlines()


#定义刷新商品信息的函数
def refresh_goods():
    json.dump(goods,open('../db/goods.json','w'),ensure_ascii=False,indent=1)

def refresh_user():
    json.dump(user_info,open('../db/mall_user.json','w'),ensure_ascii=False,indent=1)

#定义如果未结算退出时记录购物车信息的函数
def cache_cart(user_name):
    save_cart[user_name]=cart      #将购物车列表赋值于要保存的数据变量
    # json文件写入
    json.dump(save_cart,open('../db/mall_cart.json','w'),ensure_ascii=False,indent=1)
#定义用户注册函数
def regis():
    #设置退出标识符
    exit_flag=0
    while exit_flag==0:
        user_name=input('请输入您的用户名:')
        if user_name in user_info.keys():
            print('此用户已被注册,请重新输入.')
        else:
            user_pwd=input('请输入您的密码:')
            for i in range(3):
                user_pwd_again=input('请再次确认您的密码:')
                if user_pwd_again==user_pwd:
                    #赋值密码变量
                    user_info[user_name]=[user_pwd_again,0,[]]
                    #将变量写入user_info文件
                    refresh_user()
                    print('用户名%s已注册成功,请登录购买商品...'%user_name)
                    exit_flag=1
                    break
                elif i==2:
                    print('您输入的密码次数超过三次,注册关闭!')
                    exit_flag=1
                else:
                    print('您输入的密码和上次输入的密码不匹配,请重新输入,还有%s次机会.'%(2-i))
#定义用户充值函数
def refill(user_name):
    for i in range(3):
        amount=input('请输入您要充值的金额,请输入数字:')
        if amount.isdigit():
            result=terminal_pay.pay_api(int(amount),'大牛逼商城',)
            if result:
                user_info[user_name][1]+=int(amount)
                #写入用户的json文件中
                refresh_user()
                print('\033[32;1m土豪,请保养程序员!!!\033[0m充值成功,您的余'
                      '额为\033[31;1m%s\033[0m'%user_info[user_name][1])
                #打印余额
                balance=user_info[user_name][1]
                print(balance)
                break
            else:
                print('充值失败,请联系最屌银行行长')
                break
        elif i==2:
            exit('你在坑我么?告诉你要输入数字的,程序关闭...')
        else:
            print('您输入的不是数字,请重新输入..')
#定义显示购物车函数
def show_vcart(cart):
    # print(cart)
    if len(cart)>0:
        #将内存中的购物车列表计算重复数量
        v_cart = collections.Counter(cart)
        #转化为字典,方便取值
        dv_cart=dict(v_cart)
        #使用prettytable 显示购物车信息
        row=prettytable.PrettyTable()
        row.field_names=['序列号','商品名称','商品数量','商品总价']
        for i in enumerate(dv_cart):
            index=i[0]
            item=i[1][0]
            totle_price = i[1][1] * dv_cart[i[1]]
            item_amount = dv_cart[i[1]]
            row.add_row([index,item,item_amount,totle_price])
        print(row)
    else:
        print('\033[31;1m购物车为空\033[0m'.center(50,'*'))
    time.sleep(1)
#定义付款结算函数
def check_cart():
    while True:
        inp = input('''1.余额支付
2.信用卡支付
选择支付类型:''')
        if inp == '1':
            if len(cart)>0:
                v_cart=collections.Counter(cart)
                dv_cart=dict(v_cart)
                #定义空列表
                ddv_cart=[]
                #遍历字典,将字典中的元素添加入空列表
                for i in enumerate(dv_cart):
                    index=i[0]
                    item=i[1][0]
                    totle_price = i[1][1] * dv_cart[i[1]]
                    item_amount = dv_cart[i[1]]
                    ddv_cart.append([item,item_amount,totle_price])
                #改变json数据中的变量值,记录购物历史
                user_info[user_name][2].append([time_now,ddv_cart])
                #更改余额
                user_info[user_name][1]=balance
                #更爱用户余额,写入购物历史数据,更改商品库存
                refresh_user()
                refresh_goods()
                #清空购物车中的商品
                cart.clear()
                #将清空的购物车信息写入二次登陆的用户信息
                cache_cart(user_name)
                print('\033[31;1m结账成功,波多野结衣即将为您送货,请准备收货...\033[0m')
                time.sleep(1)
                break
            else:
                print('\033[31;1m购物车是空的...\033[0m')
                #如果为空,重置二次登陆用户的购物车信息
                cache_cart(user_name)
                time.sleep(1)
                break
            # break
            # return True
        elif inp == '2':
            if len(cart)>0:
                # print(cart)
                pri_list=[]
                for item in cart:
                    pri_list.append(item[1])
                sum_amount=sum(pri_list)
                result=terminal_pay.pay_api(sum_amount,'大牛逼商城',)
                if result:
                    v_cart=collections.Counter(cart)
                    dv_cart=dict(v_cart)
                    #定义空列表
                    ddv_cart=[]
                    #遍历字典,将字典中的元素添加入空列表
                    for i in enumerate(dv_cart):
                        index=i[0]
                        item=i[1][0]
                        totle_price = i[1][1] * dv_cart[i[1]]
                        item_amount = dv_cart[i[1]]
                        ddv_cart.append([item,item_amount,totle_price])
                    #改变json数据中的变量值,记录购物历史
                    user_info[user_name][2].append([time_now,ddv_cart])
                    #更爱用户余额,写入购物历史数据,更改商品库存
                    refresh_user()
                    refresh_goods()
                    #清空购物车中的商品
                    cart.clear()
                    #将清空的购物车信息写入二次登陆的用户信息
                    cache_cart(user_name)
                    print('\033[31;1m结账成功,波多野结衣即将为您送货,请准备收货...\033[0m')
                    time.sleep(1)
                    break

                else:
                    print('信用卡支付失败!!!')
                    time.sleep(1)
                    break
            else:
                print('\033[31;1m购物车是空的...\033[0m')
                time.sleep(1)
                break


#定义查看购物历史函数
def show_his(user_name):
    user_info=json.load(open('../db/mall_user.json','r'))
    #购物历史数据变量赋值
    his_list=user_info[user_name][2]
    #入购物历史为空的处理
    if len(his_list)==0:
        print('无购物历史...')
    else:
        for his in his_list:
            #取值时间戳
            dt=his[0]
            print('\033[31;1m购物时间:%s\033[0m'.center(50,'*')%dt)
            #打印购买详情
            row=prettytable.PrettyTable()
            row.field_names=['商品名称','数量','总额']
            for item in his[1]:
                #变量取值
                p_name=item[0]
                p_amount=item[1]
                p_totle=item[2]
                row.add_row([p_name,p_amount,p_totle])
            print(row)
#定义编辑购物车函数,后期追加的功能,所以代码比较多,跟之前写的耦合性较弱
def edit_cart(user_name):
    #定义变量,用set的方式去重,并转化为列表,作为商品信息
    e_cart=list(set(cart))
    e_vcart=collections.Counter(cart)
    e_vcart=dict(e_vcart)
    #将列表排序,方便取值
    e_cart.sort()
    #打印购物车信息
    row=prettytable.PrettyTable()
    row.field_names=['商品序列号','商品名称','商品数量','总价']
    for i in enumerate(e_cart):
        index=i[0]
        p_name=i[1][0]
        p_price=i[1][1]
        p_amount=e_vcart[i[1]]
        p_totle=i[1][1]*e_vcart[i[1]]
        p_belong=i[1][2]
        row.add_row([index,p_name,p_amount,p_totle])
    print(row)
    while True:
        #用户选择商品序列
        choice_num=input('请输入要编辑的商品序列号,输入\033[31;1mq或quit\033[0m为退出编辑购物车:')
        #设置条件,输入为数字,并且小于商品列表的数量
        if choice_num.isdigit() and  int(choice_num)<len(e_cart):
            #变量赋值
            choice_num=int(choice_num)
            goods_stock=goods[e_cart[choice_num][2]][e_cart[choice_num][0]]['stock']
            p_amount=e_vcart[e_cart[choice_num]]
            balance=user_info[user_name][1]
            print('目前商品库存量为\033[32;1m%s\033[0m'%goods_stock)
            while True:
                choice_num_d=input('输入要购买的商品数量:')
                if choice_num_d.isdigit():
                    choice_num_d=int(choice_num_d)
                    if choice_num_d<=goods_stock:
                        if choice_num_d==p_amount:
                            print('修改商品数量成功')
                            break
                        elif choice_num_d>p_amount:
                            #计算差价
                            d_price=int(choice_num_d-p_amount)*int(e_vcart[e_cart[choice_num]])
                            if balance>=d_price:
                                for i in range(choice_num_d-p_amount):
                                    cart.append(e_cart[choice_num])
                                #使用差价计算余额
                                balance-=d_price
                                #修改库存信息
                                goods_stock+=p_amount
                                goods_stock-=choice_num_d
                            else:
                                print('余额不足,修改失败,请充值!')
                                break
                        else:
                            d_price=int(abs(choice_num_d-p_amount))*(e_vcart[e_cart[choice_num]])
                            for i in range(abs(choice_num_d-p_amount)):
                                cart.remove(e_cart[choice_num])
                            #计算差价,修改库存,余额
                            balance+=d_price
                            goods_stock+=p_amount
                            goods_stock-=choice_num_d
                            print('修改成功.')
                            break
                    else:
                        print('输入数量有误,请合适商品的库存...')
                        break
                else:
                    print('输入类型有误请重新输入...')
                    break
        elif choice_num == 'q' or choice_num == 'quit':
            print('退出编辑购物车...')
            break
        else:
            print('输入有误,请重新输入...')



def main():
    #设置退出循环标识符初始值
    break_flag=0
    #程序开始,输入用户名
    name=input('请输入\033[31;1m壕\033[0m的用户名:')
    global user_name
    user_name=name
    if  user_name in locker:
        #退出并回显
        exit('用户已被锁定')
    #判断是否在为已注册用户并且未被锁定
    elif user_name in user_info.keys() and user_info not in locker:
        for i in range(3):
            #退出标识符是否被改变
            if break_flag==1:
                #如改为1退出循环
                break
            else:
                #确认密码
                pwd=input('请输入%s的密码:'%user_name)
                if pwd==user_info[user_name][0]:
                    #判断是否有未结算退出的购物清单
                    global cart
                    if save_cart.get(user_name)==None:
                        #如果空,将购物车设置为空
                        cart=[]
                    else:
                        #反之,将读取未结算商品列表
                        cart=save_cart[user_name]
                        for i in range(len(cart)):
                            cart[i]=tuple(cart[i])
                    print('登陆成功...')
                    print('欢迎来到大牛逼商城,走过路过,不要错过...'.center(50,'*'))
                    while break_flag==0:
                        #判断购物车是否为空,设置余额初始值
                        global balance
                        if save_cart.get(user_name)==None or len(save_cart[user_name])<=0:
                            balance = user_info[user_name][1]
                            print('壕,您的账户余额为:\033[31;1m%s\033[0m,\033[32;1m(钱不够?账户'
                                  '充值请输入r,回车继续购物)\033[0m:'%balance)
                        else:
                            #如果购物车不为空,计算扣除商品总价后的余额初始
                            cart_price_list=[]
                            for i in cart:
                                cart_price_list.append(i[1])
                            # balance=user_info[user_name][1]-sum(cart_price_list)
                            print('\033[31;1m您的购物车中还有未结算的商品,如减去购物车'
                                  '中的商品总价,您的余额为\033[0m\033[31;1m%s\033[0m'%balance)
                            time.sleep(1)
                        #显示购物主菜单
                        mrow=prettytable.PrettyTable()
                        mrow.field_names=['功能','购物','查看购物车','查看购物历史',
                                          '余额充值','退出购物商城','确认购买','编辑购物车']
                        mrow.add_row(['快捷键','回车','S或showcart','H或history',
                                      'R或refill','Q或quit','C或check','E或者edit'])
                        print(mrow)
                        menu=input('''\033[32;1m选择菜单:\033[0m''')
                        #判断用户选择
                        if menu.lower()=='r':
                            refill(user_name)   #执行充值函数
                        elif menu.lower()=='h' or menu.lower()=='history':
                            time.sleep(1)
                            show_his(user_name) #执行查看购物历史记录函数
                            time.sleep(1)
                        elif menu.lower()=='s' or menu.lower()=='showcart' :
                            time.sleep(1)
                            show_vcart(cart)    #执行查看购物车函数
                        elif menu.lower()=='c' or menu.lower()=='check':
                            check_cart()
                        elif menu.lower()=='q' or menu.lower()=='quit':
                            cache_cart(user_name)   #执行未结算退出保存购物清单函数
                            exit('已退出商城')
                        elif menu.lower()=='e' or menu.lower()=='edit':
                            edit_cart(user_name)    #执行编辑购物车函数
                        elif len(menu)==0:      #判断输入为回车
                            while break_flag==0:
                                print('壕,您的扣除购物车中的钱款预计账户余额为:\033[31;1m%s\033[0m:'%balance)
                                print('请选择商品的类型编号'.center(50,'='))
                                cla_list=list(goods.keys())     #将分类转化为列表
                                #打印商品分类
                                for i in cla_list:
                                    print(cla_list.index(i),i)
                                #让用户选择分类序列号
                                choice_cla_num=input('\033[32;1m请选择您要购买物品类型所对'
                                '应的序列号(返回主菜单输入b或back,查看购物车输入s,确认付款输入c,退出输入q或quit):\033[0m')
                                #判断用户输入的类型,如果为数字并且数字小于列表元素数量
                                if choice_cla_num.isdigit() and int(choice_cla_num)<len(cla_list):
                                    #设置变量
                                    choice_cla_num=int(choice_cla_num)
                                    cla=cla_list[choice_cla_num]
                                    goods_list=list(goods[cla])     #取出对应的商品列表
                                    while break_flag==0:
                                        print('壕,您的预计账户余额为:\033[31;1m%s\033[0m'%balance)
                                        row=prettytable.PrettyTable()
                                        row.field_names=['序列号','商品名称','商品价格','商品库存']
                                        for p in goods_list:
                                            p_num=goods_list.index(p)
                                            p_name=p
                                            p_price=goods[cla][p]['price']
                                            p_stock=goods[cla][p]['stock']
                                            row.add_row([p_num,p_name,p_price,p_stock])
                                        print(row)
                                        #用户选择物品编号
                                        choice_p_num=input('\033[32;1m输入您要购买的商品序列号,返回商品分类请输入'
                                                           'b或back,查看购物车输入s,确认付款输入c,退出系统输入q或quit:\033[0m')
                                        if choice_p_num.isdigit() and int(choice_p_num)<len(goods_list):
                                            #定义变量
                                            p_name=goods_list[int(choice_p_num)]
                                            p_price=goods[cla][p_name]['price']
                                            p_stock=goods[cla][p_name]['stock']
                                            p_belong=goods[cla][p_name]['belong']
                                            while break_flag==0:
                                                p_count=input('\033[32;1m输入您要购买的商品数量,直接回车系统默认数量默1:\033[0m')
                                                #判断库存
                                                if len(p_count)==0:
                                                    p_count=1
                                                elif p_count.isdigit():
                                                    if int(p_count) <= p_stock:
                                                        p_count = int(p_count)
                                                    else:
                                                        print('库存数量有限,最大购买数量为%s' % p_stock)
                                                        break
                                                #余额大于商品总价
                                                # if balance >= p_count*p_price:
                                                p_stock-=p_count
                                                goods[cla][p_name]['stock']=p_stock
                                                #加入购物车
                                                for i in range(p_count):
                                                    cart.append((p_name,p_price,p_belong))
                                                print('商品\033[32;1m%s\033[0m已加入购物车'%p_name)
                                                v_cart=collections.Counter(cart)
                                                print('\033[31;1m未付款商品\033[0m'.center(50,'*'))
                                                #显示购物车
                                                show_vcart(v_cart)
                                                #余额减去商品总价
                                                balance-=p_count*p_price
                                                break
                                        elif choice_p_num.lower()=='b' or choice_p_num.lower=='back':
                                            break
                                        elif choice_p_num.lower()=='s':
                                            show_vcart(cart)    #查看购物车
                                        elif choice_p_num.lower()=='c' or choice_p_num.lower()=='check':
                                            check_cart()        #确认支付
                                        elif choice_p_num.lower()=='q' or choice_p_num.lower()=='quit':
                                            cache_cart(user_name)
                                            exit('已退出商城')
                                        else:
                                            print('输入类型错误,请重新输入')
                                            time.sleep(1)
                                elif choice_cla_num.lower()=='s'or choice_cla_num.lower()=='showcart':
                                    show_vcart(cart)    #查看购物车
                                elif choice_cla_num.lower()=='c' or choice_cla_num.lower()=='check':
                                    check_cart()
                                elif choice_cla_num.lower()=='b'or choice_cla_num.lower()=='back':
                                    break
                                elif choice_cla_num.lower()=='q' or choice_cla_num.lower()=='quit':
                                    break_flag=1
                                    cache_cart(user_name)
                                elif choice_cla_num.lower()=='e' or choice_cla_num.lower()=='edit':
                                    edit_cart(user_name)    #编辑购物车
                                else:
                                    print('输入有误,请重新输入')
                #输入密码超过三次,用户锁定,并写入被锁用户名单文件
                elif i==2:
                    user_lock.write('\n%s'%user_name)
                    user_lock.close()
                    exit('三次密码错误,账户已被锁定')
                else:
                    print('密码错误,请重新输入...')
    else:
        #用户注册选项
        y_or_n=input('没有此用户名,需要注册才能进入商城!!!'
                     '是否要注册?\033[31;1m输入y或者回车为注册,n或者q退出\033[0m:')
        if len(y_or_n)==0 or y_or_n=='y':
            regis()     #执行用户注册函数
        elif y_or_n=='n' or y_or_n=='q':
            exit('程序退出...')
        else:
            exit('输入错误,程序退出...')

if __name__ == '__main__':
    main()