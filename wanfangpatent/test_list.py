import datetime
import random
if __name__ == '__main__':

    li = [1,2,3,4,5,6]
    if li is not None:
        print('sucsess')
    else:
        print('lalal')
    print(isinstance(li,list))
    print("""select * from sd_patent where applynumber = %s""" %'nihao')
    name = 'afgh'
    print("""UPDATE orgnizations SET num =%d WHERE orgnization_name = %s""" % (1, name))
    print(random.randint(10, 17))
    name = 'lalal'
    name = '作者单位:(%s)' % name
    print(name)
    dt = datetime.datetime.now()