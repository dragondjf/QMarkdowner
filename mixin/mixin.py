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
