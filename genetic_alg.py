import sqlite3
import time
import numpy as np
import pandas as pd
import matplotlib as plt

raletive_paths= "template_For_Data_Prediction\\"
def get_path(path):
    global raletive_paths
    raletive_paths = path

class EMS_data:
    path = None
    def __init__(self, pop_size, chromosome_size,raletive_path=None):
        global raletive_paths
        #path = raletive_path
        self.path = raletive_paths
        #初始化种群，需要输入种群大小pop_size和染色体大小chromosome_size
        self.pop_size = pop_size
        self.chromosome_size = chromosome_size
        self.population = np.round(np.random.rand(pop_size, chromosome_size)).astype(int)
        self.fit_value = np.zeros((pop_size, 1))
        self.data_init()


    def select_chromosome(self):
        #进行自然选择，现在是fit_value争取最小
        total_fitness_value = self.fit_value.sum()
        p_fit_value = (self.fit_value.max()+self.fit_value.min()-self.fit_value)/total_fitness_value
        p_fit_value = np.cumsum(p_fit_value)
        point = np.sort(np.random.rand(self.pop_size, 1), 0)
        fit_in = 0                                  
        new_in = 0
        new_population = np.zeros_like(self.population)
        while new_in < self.pop_size and fit_in < self.pop_size:
            if point[new_in] < p_fit_value[fit_in]:
                new_population[new_in, :] = self.population[fit_in, :]
                new_in += 1
            else:
                fit_in += 1
        self.population = new_population

    def cross_chromosome(self, cross_rate):
        #染色体的交叉
        x = self.pop_size
        y = self.chromosome_size
        new_population = np.zeros_like(self.population)
        for i in range(0, x-1, 2):
            if np.random.rand(1) < cross_rate:
                insert_point = int(np.round(np.random.rand(1) * y).item())
                new_population[i, :] = np.concatenate([self.population[i, 0:insert_point], self.population[i+1, insert_point:y]], 0)
                new_population[i+1, :] = np.concatenate([self.population[i+1, 0:insert_point], self.population[i, insert_point:y]], 0)
            else:
                new_population[i, :] = self.population[i, :]
                new_population[i + 1, :] = self.population[i + 1, :]
        self.population = new_population

    def best(self):
        #选择最好的个体
        best_individual = self.population[0, :]
        best_fit = self.fit_value[0]
        for i in range(1, self.pop_size):
            #现在是个体fit_value越小容易被选择
            if self.fit_value[i] < best_fit:
                best_individual = self.population[i, :]
                best_fit = self.fit_value[i]
        return best_individual, best_fit

    def mutation_chromosome(self, mutation_rate):
        #染色体变异
        x = self.pop_size
        for i in range(x-1):
            if np.random.rand(1) < mutation_rate:
                m_point = int(np.round(np.random.rand(1) * self.chromosome_size).item())
                if self.population[i, m_point] == 1:
                    self.population[i, m_point] = 0
                else:
                    self.population[i, m_point] = 1

    def binary2decimal(self, population:np.ndarray) -> np.ndarray:
        #把一个个体的其中24个部分的二进制数(10个整数位，4个小数位)转换成24个部分的十进制数
        if population.ndim != 1:
            population = population[0]
        y = self.chromosome_size
        ans = np.zeros(y//14)
        #计算每一个对应的fit_value值
        for k in range(0,y//14):
            mid = 0
            for i in range(0,14):
                mid += 2 ** (9-i) * population[k*14+i]
            ans[k] = mid
            #归一化
            if(k <=23):
                ans[k] = (mid/512)*100 - 50
            else:
                ans[k] = (mid/1024)*50
        return ans

    def cal_obj_value(self):
        #用来计算个体的fit_value
        y = self.pop_size
        for i in range(y):
            self.fit_value[i] = self.function(self.binary2decimal(self.population[i]))
        return 0

    def data_init(self):
        # Load是负荷
        # PV是光伏发电
        # WT是风力发电
        # price就是电价
        print(self.path+"load.txt")
        self.Load = pd.read_csv(self.path+"load.txt",delimiter = "\t",header = None)
        self.PV = pd.read_csv(self.path+"PV.txt",delimiter = "\t",header = None)
        self.WT = pd.read_csv(self.path+"WT.txt", delimiter="\t", header=None)
        self.price = pd.read_csv(self.path+"电价.txt", delimiter="\t", header=None)
        self.grid_P = pd.Series([0.0]*24) #24小时电网交互功率
        self.grid_C = pd.Series([0.0]*24) #电网交互费用
        self.bat_E = pd.Series([0.0]*24) #蓄电池电量
        self.car_E = pd.Series([0.0]*24) #汽车用电量
        self.remain = -self.Load + self.PV + self.WT


    def function(self,X):
        #计算，返回值是消耗的电价
        #约束条件是
        # 风能发电PV，光伏发电WT，用电载荷Load，储能模块充电/放电bat_E，电动汽车用电car_E，电网输出/流入电量grid_P
        #PV + WT + bat_E + grid_P = Load + car_E
        bat_Emax = 551.8 #蓄电池最大电量
        bat_Emin = 0.4 * bat_Emax #要求蓄电池最少要有40%的电量储备
        bat_E0 = 0.8 * bat_Emax #假定初始时有80%的电量
        car_Emax = 500 #电车最大充电量
        car_Emin = 0 #电车供电不能为负
        car_E0 = car_Emax * 0.25 #电车初始电量
        total_cost = pd.Series([0.0]*24)
        for i in range(0,24):
            if(i == 0):
                self.bat_E[1] = bat_E0 *(1-0.0001) + X[1]*0.9 #储能功率
                self.car_E[1] = car_E0 *(1-0.0002) + X[24]*0.9
            else:
                self.bat_E[i] = self.bat_E[i-1]*(1-0.0001)+X[i]*0.9
                self.car_E[i] = self.car_E[i-1]*(1-0.0002) + X[i+24]*0.9
            self.grid_P[i]= self.remain.iat[i,0] - X[i] - X[i+24]# 交互功率
            self.grid_C[i] = self.price.iat[i,0] * self.grid_P[i]# 购电成本
            #总共的消耗 = 电网购电成本/售电收入 - 风力发电收入 -汽车充电收入 - 光伏发电收入 + 储能超标惩罚 + 汽车用电超标惩罚
            total_cost[i] = (self.grid_C[i] - self.PV.iat[i,0]*0.0096 - self.car_E[i]*0.02 -
                      self.WT.iat[i,0]*0.0296 + 10000*abs(max(0,self.bat_E[i] - bat_Emax)) + 1000*abs(min(0,self.bat_E[i] - bat_Emin)) + 10000*abs(max(0,self.car_E[i] - car_Emax)) + 1000*abs(min(0,self.car_E[i] - car_Emin)))
        return(total_cost.sum())

def GA_run_func(path=None):
    print("data processing...")
    cross_rate = 0.8
    mutation_rate = 0.001
    MAXGEN =75
    pop_size = 100
    chromosome_size = 48*14 #10位整数位 4位小数位
    population = EMS_data(pop_size,chromosome_size,path)
    x_array:np.ndarray = np.zeros(MAXGEN)
    ever_best_individiual, ever_best_fit = population.best()

    for i in range(MAXGEN):
        population.cal_obj_value()
        population.select_chromosome()
        population.cross_chromosome(cross_rate)
        population.mutation_chromosome(mutation_rate)
        best_individual, best_fit = population.best()
        if (i == 1):
            ever_best_individiual, ever_best_fit = population.best()
        else:
            if(ever_best_fit > best_fit):
                ever_best_individiual, ever_best_fit = best_individual, best_fit
        best_individual = np.expand_dims(best_individual, 0)
        x = population.binary2decimal(best_individual)
        x_array[i] = population.function(x)
        print(f"现在的大小是{x_array[i]}")
        if(i == MAXGEN-1):
            final = population.binary2decimal(ever_best_individiual)
            print(f"本轮运算完成，最终的结果是{final}，它的计算值是{population.function(final)}")
            database_input(final,"BatteryChange")
            database_input(x_array, "x_values")
            return final
        time.sleep(1)


def database_input(arr:np.ndarray, str):
    print("data processing...")
    conn = sqlite3.connect('data/data_db.db')
    c = conn.cursor()
    c.execute("PRAGMA table_info(dataTable)")
    columns = [column[1] for column in c.fetchall()]
    if str not in columns:
        c.execute(f"ALTER TABLE dataTable ADD COLUMN {str} REAL")
    for i, value in enumerate(arr):
        c.execute(f"UPDATE dataTable SET {str} = {value} WHERE rowid = {i+1}")
    conn.commit()
    conn.close()
    print("储能数据发送到数据库！")


if  __name__ =="__main__":
    GA_run_func()


