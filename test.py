'''
Created on 10 Apr 2012

@author: Will
'''

def return_list(a):
        return a
        

if __name__ == '__main__':
        a = [1,2,3]
        b = return_list(a)
        del a[0]
        print a
        print b