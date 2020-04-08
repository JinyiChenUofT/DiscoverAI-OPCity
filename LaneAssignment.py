import math


class LaneAssignment:
    def calculate_speed(self, estimate_rate_of_traffic, Kj, Uf, lane_number):
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

    def assign_lanes(self, estimate_rate_of_traffic1, estimate_rate_of_traffic2, Kj, Uf, max_lane_number) -> int:
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

        print("Direction 1\t\t\t\t\t\t\t Direction 2")
        temp_U = (0, 0)
        for n in range(1, max_lane_number):
            temp_U = (self.calculate_speed(estimate_rate_of_traffic1, Kj, Uf, n),
                      self.calculate_speed(estimate_rate_of_traffic2, Kj, Uf, max_lane_number - n))

            print("# of lane: %d, speed: %f \t # of lane: %d, speed: %f" % (
                n, temp_U[0], max_lane_number - n, temp_U[1]))


# estimate_rate_of_traffic1, estimate_rate_of_traffic2, Kj, Uf, max_lane_number
# 假设往北方向车流量 100 vehicles/hour, 往南 400 vehicles/hour, Kj = 50, 限速Uf 100km/h, 双向一共6车道
LaneAssignment().assign_lanes(100, 400, 50, 100, 6)
