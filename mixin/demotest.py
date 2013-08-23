#!/usr/bin/python
# -*- coding: utf-8 -*-

import mixin


class Demo(mixin.Mixin):
    __mixinname__ = 'Demo'
    def __init__(self):
        self.initmixin()
        self.name = 'Demo'


def add(a, b):
    return a + b


mixin.setMixin('Demo', '1', 'aaaaaaaa')
mixin.setMixin('Demo', '2', (1,2,4))
mixin.setMixin('Demo', '2', (3,4))
mixin.setMixin('Demo', '3', {1:2})
mixin.setMixin('Demo', '3', {1:3})
mixin.setMixin('Demo', '5', 'asssssssssssssssssssssssssss')
mixin.setMixin('Demo', '5', (1,2,3,45))
mixin.setMixin('Demo', '5', 'assss')
mixin.setMixin('Demo', '6', [1,2,3])
mixin.setMixin('Demo', '5', [1,2])
mixin.setMixin('Demo', 'add', add)
mixin.setMixin('Demo', 'change', 'setup.change_package_fromLib')


def main():
    d = Demo()

    print mixin.__mixinset__

    print d
    print Demo

    print dir(d)
    print dir(Demo)

    print d.__dict__
    print Demo.__dict__

    print hasattr(d, 'add')
    print d.add(3, 4)

    print d.__mixins__


if __name__ == '__main__':
    main()
