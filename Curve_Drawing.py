
import numpy as np
import random
import math
from math import pi

class Computation_Curve:
    
    def __init__(self, t, P_elem):
        self.t = t      # knot vector
        self.P_elem = P_elem
        self.num_ctrl = P_elem.shape[0]
        self.degree = self.num_ctrl-1
        self.idx_list_pr = np.arange(0, self.num_ctrl, 1)
        
        self.num_t = t.shape[0]
        self.degreeB = self.num_t - self.num_ctrl - 1
    
    def Bezier_Curve(self, idx_list_pr, deg):
        # Recursive function
        
        idx_list_chl1 = idx_list_pr[0:deg]
        idx_list_chl2 = idx_list_pr[1:deg+1]
        deg -= 1
        
        if deg == 0:
            P_chl1 = self.P_elem[idx_list_chl1, :]
            P_chl2 = self.P_elem[idx_list_chl2, :]
        else:
            P_chl1 = self.Bezier_Curve(idx_list_chl1, deg)
            P_chl2 = self.Bezier_Curve(idx_list_chl2, deg)
        
        P_pr = (1-self.t)*P_chl1 + self.t*P_chl2
        
        return P_pr
    
    def BSpline_Curve(self):
        
        BSpline = np.zeros([self.num_t,2])
        for i in range(0, self.num_ctrl):
            BSpline = self.P_elem[i,:] * self.BFunction(i,self.degreeB)
            
        return BSpline
            
    def BFunction(self, pos, deg):
        # Recursive function

        if deg == 0:
            B = np.zeros([self.num_t,1])
            for j in range(0, self.num_t):
                if self.t[j]>=self.t[pos] and self.t[j]<self.t[pos+1]:
                    B[j] = 1
                else:
                    B[j] = 0
        else:
            B = (self.t-self.t[pos])/(self.t[pos+deg]-self.t[pos]) * self.BFunction(pos,deg-1) + \
                (self.t[pos+deg+1]-self.t)/(self.t[pos+deg+1]-self.t[pos+1]) * self.BFunction(pos+1,deg-1)
        
        return B


class Bezier_Polygon():
    
    def __init__(self, Connect_Point, num_connect, angle_buff, r_range):
        # Calculate the angle range of control point P2
        
        self.num_connect = num_connect
        self.angle_buff = angle_buff
        self.r_range = r_range
        
        # compute angular coords of connect point
        Connect_Vector = np.zeros((num_connect, 2))
        for i in range(0, num_connect):
            if i == num_connect-1:
                i_plus = 0
            else:
                i_plus = i + 1
            Connect_Vector[i,:] = Connect_Point[i_plus,:] - Connect_Point[i,:]
        theta = np.arctan2(Connect_Vector[:,1], Connect_Vector[:,0])

        # compute angle between lines
        Norm_C = np.linalg.norm(Connect_Vector, axis=1)
        cos_val = np.zeros(num_connect)
        for i in range(0, num_connect):
            if i == num_connect-1:
                i_plus = 0
            else:
                i_plus = i + 1
            cos_val[i] = np.dot(Connect_Vector[i,:],-Connect_Vector[i_plus,:])/(Norm_C[i]*Norm_C[i_plus])
        theta_int = np.arccos(cos_val)

        # calculate start position anglea
        self.theta_st = theta - theta_int/2
        

    def Phase_ContolPoint(self):
        #  Define the initial and last state of control point P2
        
        r_list = np.random.uniform(self.r_range[0], self.r_range[1], self.num_connect)
        
        theta_list = np.zeros(self.num_connect)
        for i in range(0,self.num_connect):
                theta_list[i] = random.uniform(self.theta_st[i]-math.pi+self.angle_buff, self.theta_st[i]-self.angle_buff)
                
        phase = np.hstack((r_list, theta_list))
        return phase
                
        
def Curve2Polygon(t_vector, Connect_Point, Polar_Vector):
    # Create polygon by connecting 3 degree bezier curve
    
    num_curve = Connect_Point.shape[0]
    dim_curve = t_vector.shape[0]
        
    # define control point
    Ctrl_List = np.zeros((4*num_curve, 2))
    idx_0 = 0
    idx_nx1 = 5
    for i in range(0, num_curve):
        if i == num_curve-1:
            idx_p3 = 0
        else:
            idx_p3 = i+1
        P0 = Connect_Point[i,:]
        P3 = Connect_Point[idx_p3,:]
        
        L = np.linalg.norm(P3-P0)
        r = L * Polar_Vector[i]
        theta = Polar_Vector[i+num_curve]
        P2 = P3 + [r*np.cos(theta), r*np.sin(theta)]
        
        # P1 of next curve
        vec23 = P3 - P2
        P1_next = P3 + vec23
        
        # allocate in array
        Ctrl_List[idx_0,:]=P0; Ctrl_List[idx_0+2,:]=P2; Ctrl_List[idx_0+3,:]=P3
        Ctrl_List[idx_nx1,:] = P1_next
        
        idx_0 = idx_0 + 4;
        if i == num_curve-2:
            idx_nx1 = 1
        else:
            idx_nx1 = idx_nx1 + 4
        
    # create bezier curve
    Polygon = np.zeros((dim_curve*num_curve,2))
    idx_poly = 0
    idx_ctrl = 0
    for i in range(0, num_curve):
        
        control_point = Ctrl_List[idx_ctrl:idx_ctrl+4, :]
        Inst1 = Computation_Curve(t_vector, control_point)
        Polygon[idx_poly:idx_poly+dim_curve, :] = Inst1.Bezier_Curve(Inst1.idx_list_pr, Inst1.degree)
        
        idx_poly = idx_poly + dim_curve
        idx_ctrl = idx_ctrl + 4
        
    return Polygon
        
        
    
        
     