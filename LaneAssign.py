import math
import numpy as np
import matplotlib.pyplot as plt

class LaneAssignment:
    def calculate_speed(self, estimate_rate_of_traffic, Kj, Uf, lane_number) -> int:
        # TODO: Use optimization model instead of math calculation
        """
        Since we know the maximum number of lanes, a tricky way to do this is just do the math
        Q = KJ * U - (KJ / Uf) * U^2, where KJ = N * Kj
        can be translated to:
        U^2 - Uf * U + (Uf * Q)/(N * Kj) = 0
        Let a = Uf, b = Q/(N * Kj)
        Hence, U^2 - a*U + a*b = 0
        Then U = 0.5 * (a + sqrt(a^2 - 4ab))
        """

        b = estimate_rate_of_traffic / (lane_number * Kj)
        U = 0.5 * (Uf + math.sqrt(Uf ** 2 - 4 * Uf * b))
        return U

    def calculte_var_and_mean(self, speed_list):
        mean_list = []
        var_list = []
        for speed in speed_list:
            mean_list.append(np.mean(speed))
            var_list.append(np.var(speed))
        return mean_list, var_list
    
    def drawSpeedON2Lanes(self,lane1,lane2):
        #fig = plt.figure()
        plt.plot(lane1,lane2)
        plt.xlabel("speed on lane1")
        plt.ylabel("speed on lane2")
        plt.axis([95,100,95,100])
        plt.show()
    
    def drawAllOptions(self,speed_lane1,speed_lane2,finalOption,direction_traffic1):
        #fig = plt.figure()
        
        for i in range(len(speed_lane1)):
            if i == finalOption:
                label_string = "final choice " + str(i)
                plt.plot( [j for j in range(i+1)],speed_lane1[i], '<-', label = label_string)
                plt.plot( [j for j in range(i+1,len(speed_lane2)+1)],speed_lane2[i], '>-', label = label_string)
            else:
                plt.plot( [j for j in range(i+1)],speed_lane1[i], '<--', label = i)
                plt.plot( [j for j in range(i+1,len(speed_lane2)+1)],speed_lane2[i], '>--', label = i)

        plt.xlabel("lane")
        plt.ylabel("speed")
        plt.legend()
        plt.show()

    def assign_lanes(self, estimate_rate_of_traffic1, estimate_rate_of_traffic2, Kj, Uf, max_lane_number, direction_traffic1):
        """
        Use the model below to optimize U, the average speed of cars based on estimated traffic flow Q.
        Speed-Flow Relationship
        Q = Kj * U - (Kj / Uf) * U^2
        where
        Kj: Max density at 0 speed
        Uf: Max speed at 0 density
        In our specific case, the max density will be N * Kj for N lanes, and Uf is the speed limit of the road.
        Given Q, we need to find the N to optimize U
        """

        # Calculate possible lane assignments
        possible_assignments = []
        
        speed_lane1 = []
        speed_lane2 = []

        lane1_speeds = []
        lane2_speeds = []

        for n in range(1, max_lane_number):

            temp_U = (self.calculate_speed(estimate_rate_of_traffic1, Kj, Uf, n),
                      self.calculate_speed(estimate_rate_of_traffic2, Kj, Uf, max_lane_number - n))

            speed = [temp_U[0] for _ in range(n)] + [temp_U[1] for _ in range(max_lane_number - n)]

            speed_lane1.append([temp_U[0] for _ in range(n)])
            speed_lane2.append([temp_U[1] for _ in range(max_lane_number - n)])

            possible_assignments.append(speed)
            lane1_speeds.append(temp_U[0])
            lane2_speeds.append(temp_U[1])
        print(speed_lane1)

        #print(speed_lane2)
        #self.drawSpeedON2Lanes(lane1_speeds,lane2_speeds)    
        # print("Possible assignments: ", possible_assignments)

        # Calculate mean and var of speed for each assignment
        speed_mean, speed_var = self.calculte_var_and_mean(possible_assignments)
        # print(speed_mean, speed_var)

        # Find the optimal one
        index = speed_var.index(min(speed_var))

        self.drawAllOptions(speed_lane1, speed_lane2,index+1,direction_traffic1)
        

        # Return lane assignment in the form of (# of lane for direction 1, # of lane for direction 2)
        return index + 1, max_lane_number - index - 1

    

# estimate_rate_of_traffic1, estimate_rate_of_traffic2, Kj, Uf, max_lane_number
# 假设往北方向车流量 100 vehicles/hour, 往南 400 vehicles/hour, Kj = 50, 限速Uf 100km/h, 双向一共6车道
print(LaneAssignment().assign_lanes(100, 400, 50, 100, 6, 1))

