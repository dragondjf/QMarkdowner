如何利用Mixin对已定义的类进行方法和属性扩展
===============================================
>起因  
>> 类已经定义明确，但希望在创建实例时拓展实例的功能，这种情况下怎么办？

>目的  
>> 实现一种机制，能够根据一定的规则，在实例创建时动态的拓展实例的功能（方法和属性)；

>方式：
>>1.动态的拓展类的方法和属性，这样所有实例都具备相应功能；  
>>>  
>>>**a.** 利用python的动态特性：类也是对象，可以在运行时动态的创建它们，就像其他任何
对象一样；  
>>>**b.** 元类就是用来创建类的“东西”;
>>>> Python会在内存中通过\__metaclass__ = Foo 创建一个名字为Foo的类对象（我说的是类对象，请紧跟我的思路）,Python没有找到\__metaclass__，它会继续在父类中寻找\__metaclass__属性，并尝试做和前面同样的操作。如果Python在任何父类中都找不到\__metaclass__，它就会在模块层次中去寻找\__metaclass__，并尝试做同样的操作。如果还是找不到\__metaclass__,Python就会用内置的type来创建这个类对象。  

>>>**c.** 代码实现
>>>
    class _MetaMixin(type):
    '''
        利用元编程扩展类属性和方法，示例：
        class DemoMixin1(object):
            __mixinname__ = 'DemoMixin'
            __metaclass__ = _MetaMixin
            def __init__(self):
                pass
        这样即可将__mixinset__中收集到的__mixinname__相关的方法和属性扩展到自定义类中
        自定义的类中必须包含如下两个类属性：
            __mixinname__ = 'DemoMixin'
            __metaclass__ = _MetaMixin
    '''
    def __new__(cls, clsname, clsbases, clsdict):
        t = type.__new__(cls, clsname, clsbases, clsdict)
        mixinId = clsdict['__mixinname__']
        if mixinId in __mixinset__:
            clsdict['__mixins__'] = __mixinset__[mixinId]
            for k, v in clsdict['__mixins__'].items():
                clsdict[k] = v
            t = type.__new__(cls, clsname, clsbases, clsdict)            
        return t
>>>**d.**使用举例：
>>>
    class DemoMixin(object):
        __mixinname__ = 'DemoMixin'
        __metaclass__ = _MetaMixin
        def __init__(self):
            pass
>>>>**只须定义\__mixinname__和\__metaclass__**
>>>>>\__mixinname__:__从\__mixinset\__中获取与自己相关的方法和属性__  
>>>>>\__metaclass__：__在元类中根据\__mixinname\__拓展类的方法和属性__


>>2.动态的拓展实例的方法和属性； 

>>>**a.** 利用python的动态特性,在\__init__对实例的\__dict__进行动态扩展   
>>>**b.** 代码实现
>>>
    class Mixin(object):
        __mixinname__ = ''  #mixin interface name, all subclass need define its own __mixinname__
        def __init__(self):
            self.initmixin()
        def initmixin(self):
            '''
                1. Add every item in __mixinset__[self.__mixinname__]
                into instance of the class which inherit from Mixin
                2. Marked by class attr __mixinname__, all subclass need define its own __mixinname__
                为继承自Mixin的子类扩展__mixinset__[self.__mixinname__]中收集到的类和方法
                __mixinset__为一字典，收集扩展方法和属性集合
                __mixinname__为ID，标识旗下的方法和属性属于哪一个类
                这种方法必须在子类中定义__mixinname__
            '''
            if self.__class__.__name__ == 'Mixin':  #don't dealing Mixin class itself
                return
            if not self.__mixinname__:
                return
            if self.__mixinname__ in __mixinset__:
                self.__dict__.update(__mixinset__[self.__mixinname__])
                setattr(self, '__mixins__', __mixinset__[self.__mixinname__])
        def initmixin2(self):
            '''
                if you use this method
                Marked by class attr __name__, all subclass don't need define its own __mixinname__
                直接以__name__为ID,不需要定义__mixinname__,但必须保证__mixinset__与类一一对应
            '''
            name = self.__class__.__name__
            if name == 'Mixin':  #don't dealing Mixin class itself
                return
            if name in __mixinset__:
                self.__dict__.update(__mixinset__[name])
                setattr(self, '__mixins__', __mixinset__[name])
>>> **c.**使用说明
>>>
    class DemoMixin(Mixin):
        __mixinname__ = 'DemoMixin'
        def __init__(self):
            self.initmixin()
>>>>**必须定义\__mixinname__, 然后在\__init__执行self.initmixin()**

>>3.如何收集需要拓展的属性和方法  
>>>**a.**利用全局变量\__mixinset__收集所有需要拓展类的方法和属性，\__mixinset__
以\__mixinname__为key,以相应属性和方法为value的字典形式存在

>>>**b.**代码实现
>>>
    __mixinset__ = {}  # 收集所有需要扩展的类方法和属性
    def setMixin(mixinname, name, value):
        '''
            mixinname----ID
            name -----属性或方法名字
            value-----对应属性或方法的具体实现
            如果value为字典，则update更新相应的字典
            如果value为列表，则extend拓展相应的列表
            如果value为元组，则sum增加相应的元组
        '''
        if mixinname in __mixinset__:
            mixins = __mixinset__[mixinname]
        else:
            __mixinset__[mixinname] = {}
            mixins = __mixinset__[mixinname]
        if name in mixins:
            if isinstance(mixins[name], (dict, tuple, list)) and isinstance(value, (dict, tuple, list)):
                if isinstance(mixins[name], dict) and isinstance(value, dict):
                    mixins[name].update(value)
                elif isinstance(mixins[name], list) and isinstance(value, list):
                    mixins[name].extend(value)
                elif isinstance(mixins[name], tuple) and isinstance(value, tuple):
                    mixins[name] = mixins[name] + value
            else:
                mixins[name] = value
        else:
            mixins[name] = value
>>>**c.** 使用举例  
>>>>收集属性和方法
>>>
    def add(a, b):
        return a + b
    setMixin('DemoMixin', '1', 'aaaaaaaa')
    setMixin('DemoMixin', '2', (1,2,4))
    setMixin('DemoMixin', '2', (3,4))
    setMixin('DemoMixin', '6', [1, 2, 3])
    setMixin('DemoMixin', '6', [7, 8, 9])
    setMixin('DemoMixin', '3', {1:2})
    setMixin('DemoMixin', '3', {1:3})
    setMixin('DemoMixin', '5', 'asssssssssssssssssssssssssss')
    setMixin('DemoMixin', '5', (1,2,3,45))
    setMixin('DemoMixin', '5', 'assss')
    setMixin('DemoMixin', '5', [1,2])
    setMixin('DemoMixin', 'add', add)
    import os
    setMixin('DemoMixin', 'getcwd111', os.getcwd)

>>4.测试Demo演示：
>>> **a.**测试代码
>>>
    class DemoMixin1(object):
        __mixinname__ = 'DemoMixin'
        __metaclass__ = _MetaMixin
        def __init__(self):
            pass
    class DemoMixin2(Mixin):
        __mixinname__ = 'DemoMixin'
        def __init__(self):
            self.initmixin()
    def main():
        d1 = DemoMixin1()
        print dir(DemoMixin1)
        print DemoMixin1.__dict__
        print dir(d1)
        print d1.__dict__
        print '-' * 20
        d2 = DemoMixin2()
        print dir(DemoMixin2)
        print DemoMixin2.__dict__
        print dir(d2)
        print d2.__dict__
    if __name__ == '__main__':
        main()
>>>>**测试结果过大，不做显示，自己可以运行下面的完整demo程序查看结果**

>>>**b.**完整代码Demo
>>>
    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    '''
        目的：当实例创建时，根据收集到的配置对相应的类进行动态方法和属性扩展
        方式有两种：
            第一种：直接扩展类属性和方法，这种方式使用元编程__new__实现较好；
                    直接拓展类clsdict，因为clsdict中存放的即为所有类属性和方法的集合
            第二种：直接扩展实例属性和方法，这种方式在初始化__init__中实现较好；
                    直接拓展实例__dict__,因为__dict__中存放的即为所有实例属性和方法的集合
    '''
    __mixinset__ = {}  # 收集所有需要扩展的类方法和属性
    class Object_Dict(dict):
        '''
            Makes a dictionary behave like an object.
        '''
        def __init__(self, *args, **kw):
            dict.__init__(self, *args, **kw)
            self.__dict__ = self
    class _MetaMixin(type):
        '''
            利用元编程扩展类属性和方法，示例：
            class DemoMixin1(object):
                __mixinname__ = 'DemoMixin'
                __metaclass__ = _MetaMixin
                def __init__(self):
                    pass
            这样即可将__mixinset__中收集到的__mixinname__相关的方法和属性扩展到自定义类中
            自定义的类中必须包含如下两个类属性：
                __mixinname__ = 'DemoMixin'
                __metaclass__ = _MetaMixin
        '''
        def __new__(cls, clsname, clsbases, clsdict):
            t = type.__new__(cls, clsname, clsbases, clsdict)
            mixinId = clsdict['__mixinname__']
            if mixinId in __mixinset__:
                clsdict['__mixins__'] = __mixinset__[mixinId]
                for k, v in clsdict['__mixins__'].items():
                    clsdict[k] = v
                t = type.__new__(cls, clsname, clsbases, clsdict)            
            return t
    class Mixin(object):
        __mixinname__ = ''  #mixin interface name, all subclass need define its own __mixinname__
        def __init__(self):
            self.initmixin()
        def initmixin(self):
            '''
                1. Add every item in __mixinset__[self.__mixinname__]
                into instance of the class which inherit from Mixin
                2. Marked by class attr __mixinname__, all subclass need define its own __mixinname__
                为继承自Mixin的子类扩展__mixinset__[self.__mixinname__]中收集到的类和方法
                __mixinset__为一字典，收集扩展方法和属性集合
                __mixinname__为ID，标识旗下的方法和属性属于哪一个类
                这种方法必须在子类中定义__mixinname__
            '''
            if self.__class__.__name__ == 'Mixin':  #don't dealing Mixin class itself
                return
            if not self.__mixinname__:
                return
            if self.__mixinname__ in __mixinset__:
                self.__dict__.update(__mixinset__[self.__mixinname__])
                setattr(self, '__mixins__', __mixinset__[self.__mixinname__])
        def initmixin2(self):
            '''
                if you use this method
                Marked by class attr __name__, all subclass don't need define its own __mixinname__
                直接以__name__为ID,不需要定义__mixinname__,但必须保证__mixinset__与类一一对应
            '''
            name = self.__class__.__name__
            if name == 'Mixin':  #don't dealing Mixin class itself
                return
            if name in __mixinset__:
                self.__dict__.update(__mixinset__[name])
                setattr(self, '__mixins__', __mixinset__[name])
    def setMixin(mixinname, name, value):
        '''
            mixinname----ID
            name -----属性或方法名字
            value-----对应属性或方法的具体实现
            如果value为字典，则update更新相应的字典
            如果value为列表，则extend拓展相应的列表
            如果value为元组，则sum增加相应的元组
        '''
        if mixinname in __mixinset__:
            mixins = __mixinset__[mixinname]
        else:
            __mixinset__[mixinname] = {}
            mixins = __mixinset__[mixinname]
        if name in mixins:
            if isinstance(mixins[name], (dict, tuple, list)) and isinstance(value, (dict, tuple, list)):
                if isinstance(mixins[name], dict) and isinstance(value, dict):
                    mixins[name].update(value)
                elif isinstance(mixins[name], list) and isinstance(value, list):
                    mixins[name].extend(value)
                elif isinstance(mixins[name], tuple) and isinstance(value, tuple):
                    mixins[name] = mixins[name] + value
            else:
                mixins[name] = value
        else:
            mixins[name] = value
    def add(a, b):
        return a + b
    setMixin('DemoMixin', '1', 'aaaaaaaa')
    setMixin('DemoMixin', '2', (1,2,4))
    setMixin('DemoMixin', '2', (3,4))
    setMixin('DemoMixin', '6', [1, 2, 3])
    setMixin('DemoMixin', '6', [7, 8, 9])
    setMixin('DemoMixin', '3', {1:2})
    setMixin('DemoMixin', '3', {1:3})
    setMixin('DemoMixin', '5', 'asssssssssssssssssssssssssss')
    setMixin('DemoMixin', '5', (1,2,3,45))
    setMixin('DemoMixin', '5', 'assss')
    setMixin('DemoMixin', '5', [1,2])
    setMixin('DemoMixin', 'add', add)
    import os
    setMixin('DemoMixin', 'getcwd111', os.getcwd)
    class DemoMixin1(object):
        __mixinname__ = 'DemoMixin'
        __metaclass__ = _MetaMixin
        def __init__(self):
            pass
    class DemoMixin2(Mixin):
        __mixinname__ = 'DemoMixin'
        def __init__(self):
            self.initmixin()
    def main():
        d1 = DemoMixin1()
        print dir(DemoMixin1)
        print DemoMixin1.__dict__
        print dir(d1)
        print d1.__dict__
        print '-' * 20
        d2 = DemoMixin2()
        print dir(DemoMixin2)
        print DemoMixin2.__dict__
        print dir(d2)
        print d2.__dict__
    if __name__ == '__main__':
        main()
>>>>**由于code中插入空行会影响排版效果，故代码相对比较紧凑，层次感有所下降**
