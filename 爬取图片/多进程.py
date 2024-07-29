from multiprocessing import Pool,cpu_count
import os
import time

def f(x):
    print("进程ID:{} 处理变量X: {}".format(os.getpid(),x))
    time.sleep(1) #主动sleep 1秒
    return x*x

if __name__ == '__main__':
    print('主进程ID:{} CPU 核数:{}'.format(os.getpid(),cpu_count()))
    st_time = time.time()
    arg_nums = list(range(1,cpu_count()+1))
    print(arg_nums)

    # 核心代码
    with Pool(cpu_count()) as p:
        p.map(f, arg_nums)

    et_time = time.time()
    print("结束了, 耗时:{}秒".format(et_time-st_time))
