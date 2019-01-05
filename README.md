# python-read-deal-write
# 多进程 #
## 目的及功能 ##
提高工作效率：python同时进行多项操作

1、用opencv读取数据

2、创建三个进程

3、用管道来传输数据

## 用法简介 ##
    fd1,fd2 = Pipe()#创建管道
    
    pool = Pool(4) #定义进程池大小 即一次性可以同时运行的进程    
    pool.apply_async(out_3Dmatrix_1,args=(fd2,)) #使用非阻塞方式调用func，阻塞是apply()

    in_road, out_road = Pipe()
    pool.apply_async(display_write,args=(in_road,)) 
        
    while True:
        try:
             print(fd1.recv())
             out_road.send("1")
        except:
            pass

    #阻塞：主程序不运行，运行完一个子程序再运行下一个子程序。
    #非阻塞：同时运行几个子程序，取决于pool大小

    pool.close() #关闭Pool，使其不再接受新的任务
    pool.join() #主进程阻塞，等待子进程的退出
