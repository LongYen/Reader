from os import set_blocking
from numpy.lib.polynomial import polyint
from numpy.linalg.linalg import norm
import xlwt  
import pandas as pd
import sys
import numpy as np
np.set_printoptions(suppress=True)

class Reader:
    def __init__(self, input_filename="input.txt",output_filename="output.xls"):
        self.input_filename = input_filename
        self.output_filename = output_filename
    
    # set rotation for the laser point to robort, R^l_r
    def setRotation(self):
        self.rotation = np.array([[1, 0, 0],
                                [0, 1, 0],
                                [0, 0, 1]],dtype=np.float64)
        return self.rotation
    
    # set translation for the laser point to robort, R^l_r
    def setTranslation(self):
        self.translation = np.array([[130], 
                                    [-130], 
                                    [0]],dtype=np.float64)
        return self.translation

    # T^b_w means that transformate body frame to world frame 
    def transformation(self, point):
        point_new = self.rotation.dot(point.reshape(3,-1)) + self.translation
        return point_new

    # Transformating txt formate to  xls formate for laser
    def txt2xls_laser(self):
        try:
            fopen = open(self.input_filename, 'r',encoding='utf-8')
            xls = xlwt.Workbook(encoding = 'utf-8')
            sheet = xls.add_sheet('value', cell_overwrite_ok=True)
            x = 0
            while True:
                line = fopen.readline()
                if not line:
                    break
                for i in range(len(line.split(","))):
                    item = line.split(",")[i]
                    item = item.split("\n")
                    sheet.write(x, i , item)
                x += 1
            fopen.close()
            xls.save(self.output_filename)  # 保存xls文件
        except:
            raise

    # Transformating txt fotmate to xls for motor
    def txt2xls_motor(self):
        try:
            fopen = open(self.input_filename, 'r',encoding='utf-8')
            xls = xlwt.Workbook(encoding = 'utf-8')
            sheet = xls.add_sheet('value', cell_overwrite_ok=True)
            x = 0
            while True:
                line = fopen.readline()
                if not line:
                    break
                for i in range(len(line.split("\t"))):
                    item = line.split("\t")[i]
                    item = item.split("\n")
                    sheet.write(x, i , item)
                x += 1
            fopen.close()
            xls.save(self.output_filename)  # 保存xls文件
        except:
            raise
    
    # get the rotation, which is from Eef frame  to  robort frame
    def getEefRoation(self):
        try:
            # Adding the header=None, because the pd.read_excel loss the one row
            output = pd.read_excel(self.output_filename, header = None)
            output=np.array(output.values[:,:],dtype=np.float64)
            for i in range(output.shape[0]):
                output[i] = self.transformation(output[i]).reshape(1,3)            
            
            
            row = output.shape[0]//3
            normal_x, normal_y, normal_z = np.zeros((3,1), dtype=np.float)
            self.vector_cross = np.zeros((20, 3, 3), dtype=np.float)

            for i in range(row):
                # normal vector,(end-start)
                normal_o = (output[3*i] + output[3*i+2])/2
                normal_x = output[3*i] - normal_o
                normal_y = output[3*i+1] - normal_o
                normal_z = np.cross(normal_x, normal_y)
                normal_x = normal_x /np.linalg.norm(normal_x)
                normal_y = normal_y /np.linalg.norm(normal_y)
                normal_z = normal_z /np.linalg.norm(normal_z)

                self.vector_cross[i, :, :] = np.c_[normal_x, normal_y, normal_z]
            print(self.vector_cross)
            return self.vector_cross

        except BaseException as e:
            print('The exception: {}'.format(e))
            sys.exit(1)


    def getEefTranslation(self):
        try:
            # Adding the header=None, because the pd.read_excel loss the one row
            output = pd.read_excel(self.output_filename, header = None)
            output = np.array(output.values[:,:],dtype=np.float64)
            for i in range(output.shape[0]):
                output[i] = self.transformation(output[i]).reshape(1,3)            
            
            
            row = output.shape[0]//3
            translation = np.zeros((20,3), dtype=np.float)

            for i in range(row):
                translation[i, :] = output[3*i]
            print(translation)
            return translation

        except BaseException as e:
            print('The exception: {}'.format(e))
            sys.exit(1)

    def getMotorDegree(self):
        try:
            # Adding the header=None, because the pd.read_excel loss the one row
            output = pd.read_excel(self.output_filename, header = None)
            output=np.array(output.values[:,:],dtype=np.float64)
            #print(self.output)
            return output

        except BaseException as e:
            print('The exception: {}'.format(e))
            sys.exit(1)  



if __name__ == "__main__":
    # put your
    reader = Reader("LaserTrack.txt", "LaserTrack.xls")  
    reader.setRotation()
    reader.setTranslation()
    reader.txt2xls_laser()
    reader.getEefRoation()
    reader.getEefTranslation()
