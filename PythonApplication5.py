import time
import cv2
from multiprocessing import Pool,Pipe


def open_camera(x_open=480,y_open=320):
    cap = cv2.VideoCapture(0)#创建一个 VideoCapture 对象
    cap.set(3,x_open)
    cap.set(4,y_open)
    return cap

def out_3Dmatrix_1(fd2):
    camera = open_camera()
    flag = 1;#设置一个标志，用来输出视频信息
    while(camera.isOpened()):#循环读取每一帧
        ret_flag , Vshow = camera.read()
        cv2.imshow("Capture_Test",Vshow)  #窗口显示，显示名为 Capture_Test（函数测试）
        k = cv2.waitKey(1) & 0xFF #每帧数据延时 a_out ms，延时不能为 0，否则读取的结果会是静态帧       
        fd2.send(Vshow)       
        time.sleep(0.1)

def display(thing):
    print(thing)

def write(thing):
    try:
        with open(r'D:\write txt\try\txt.txt', 'a') as f:
            f.write(thing)
    except:
        with open(r'D:\write txt\try\txt.txt', 'w') as f:
            f.write(thing)

def display_write(in_road):
    while True:
        try:
            thing = in_road.recv()
        except:
            pass
        else:
            display(thing)
            write(thing)
#———————————————主程序———————————
if __name__ == '__main__':
    fd1,fd2 = Pipe()
    
    pool = Pool(4) #定义进程池大小 即一次性可以同时运行的进程    
    pool.apply_async(out_3Dmatrix_1,args=(fd2,)) #使用非阻塞方式调用func，阻塞是apply()

    in_road, out_road = Pipe()
    pool.apply_async(display_write,args=(in_road,)) #使用非阻塞方式调用func，阻塞是apply()
        
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
#—————————————————————————————


