#错误定义包
class errorDefine():
    SUCCESS = 0
    NOUSER  = 1     #用户不存在
    NOSHOPID = 2    #商品不存在
    MONEYERROR=3    #提交的金额不合法
    CHANNELERROR=4  #通道错误
    ExistBindRelation=5 #已存在绑定关系
    NoBindPhone = 6#没有绑定手机
    Param       =7 #参数错误
    ErrorMoney=8 #金额错误
    NoPix=9     #没有pix账号
    NoRepayOrder = 10 #没有体现订单信息
    MoneyNotEnough=11 #体现金额不满足要求
    Other   =100    #其他错误