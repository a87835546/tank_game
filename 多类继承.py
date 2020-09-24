class A(object):
    def __init__(self):
        print('enter A print')
        print('leave A print')

class B(A):
    def __init__(self):
        print('enter B print')
        super(B, self).__init__()
        print('leave B print')

class C(A):
    def __init__(self):
        print('enter C print' + self.__class__.__name__)

        print('C父类的类名：' + C.__base__.__name__, '当前C类的类名：' + C.__name__, 'C子类的类名：' + self.__class__.__name__)
        super(C, self).__init__()
        print('leave C print' + self.__class__.__name__)

class D(B, C):
    def __init__(self):
        print('enter D print')
        super(D, self).__init__()
        print('leave D print')

d = D()