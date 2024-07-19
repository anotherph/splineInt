import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy.interpolate as spi
import csv
import argparse
from datetime import datetime, timedelta
import pandas as pd

# matplotlib.use('TkAgg')  # 또는 'Qt5Agg', 'WXAgg' 등

def loadData(str_dir):
    global x_t, y_t
    x_t = []
    x_t_ori = []
    y_t = []

    # CSV 파일 읽기
    with open(str_dir, newline='') as f:
        rdr = csv.reader(f)
        data = list(rdr)
        
        for i, line in enumerate(data):
            if i == 0:
                continue
            else:
                t_time = int(line[0][11:13])
                t_time_ori = line[0] # clocks 
                t_temp = line[1]
                
                x_t.append(t_time)
                x_t_ori.append(t_time_ori)
                y_t.append(float(t_temp))
    
    return  x_t, x_t_ori, y_t

def generate_time_intervals(array, intval):
    array_r = []
    
    interval = timedelta(minutes=intval)
    
    start_time = datetime.strptime(array[0], '%Y-%m-%dT%H:%M')
    end_time = datetime.strptime(array[-1], '%Y-%m-%dT%H:%M') + timedelta(hours=1)
  
    for time_str in array:

        while start_time < end_time:
            array_r.append(start_time.strftime('%Y-%m-%dT%H:%M'))
            start_time += interval
            # print(start_time.strftime('%Y-%m-%dT%H:%M'))

    return array_r

def runMain(args):
    
    # dir = "input_sample.csv"
    dir = f"{args.dir}"
    global x_ori, x_ori_t, y_ori
    x_ori, x_ori_t, y_ori = loadData(dir) 
    
    intval=args.intval # per minutes
    num_intval=int(60/intval) # number of interpolation per hour (1 to 60)

    x_n=np.linspace(0,x_ori[-1],len(x_ori)*num_intval)
    
    # spline interpolation
    global ipo, iy
    ipo = spi.splrep(x_ori,y_ori,k=3) # make cubic spline (k=3)
    iy=spi.splev(x_n,ipo,der=0)
    
    # save the interpolation result
    x_n_save = generate_time_intervals(x_ori_t, intval)
    y_n_save = [round(value, 1) for value in iy]
    
    # plt.plot(x_n, iy, marker='o', linestyle='-', color='b')
    # plt.plot(x_ori, y_ori, marker='o', linestyle='-', color='r')
    # plt.show()
    
    df = pd.DataFrame({
        'time': x_n_save,
        'value': y_n_save
    })
    
    # Excel 파일로 저장
    date_obj = datetime.strptime(x_n_save[0], '%Y-%m-%dT%H:%M')
    title = date_obj.strftime('%Y%m%d')
    output_file = f'{title}.csv'
    df.to_csv(output_file, index=False)

    print(f"Excel 파일 '{output_file}'이 저장되었습니다.")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('--dir', type=str, required=True, help='Directory or file path')
    parser.add_argument('--intval', type=int, required=True, help='interpolation period < 60')
    args = parser.parse_args()
    runMain(args)