#!/usr/bin/python3

class Singleton :
    __singletonptr = None

    @classmethod
    def getsingleton(cls) :
        if cls.__singletonptr == None :
            cls.__singletonptr = cls()
        return cls.__singletonptr
