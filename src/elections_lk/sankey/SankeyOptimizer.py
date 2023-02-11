import math
import random
from functools import cache, cached_property

from scipy.optimize import minimize

random.seed(1)


class SankeyOptimizer:
    @cached_property
    def default_training_data(self):
        return self.get_training_data(self.election_x, self.election_y)

    def random_init_v(self):
        X, Y, sample_weight = self.default_training_data
        dimx = len(X[0])
        dimy = len(Y[0])
        v = []
        for i in range(dimx * dimy):
            v.append(random.random())
        return v


    def build_init_v(self):
        final_result_x = self.election_x.country_final_result
        final_result_y = self.election_y.country_final_result
        total = final_result_y.summary_statistics.electors

        popular_parties_x = self.election_x.get_popular_parties(self.P_LIMIT)
        popular_parties_y = self.election_y.get_popular_parties(self.P_LIMIT)

        othered_d_x = final_result_x.party_to_votes.get_othered_dict(
            popular_parties_x
        )
        othered_d_y = final_result_y.party_to_votes.get_othered_dict(
            popular_parties_y
        )

        v = []
        for party_x in popular_parties_x + [self.NOT_COUNTED]:
            if party_x == self.NOT_COUNTED:
                vx = (
                    final_result_y.summary_statistics.electors
                    - final_result_x.summary_statistics.valid
                )
            else:
                vx = othered_d_x.get(
                    party_x,
                    0,
                )
            px = vx / total

            for party_y in self.election_y.get_popular_parties(
                self.P_LIMIT
            ) + [self.NOT_COUNTED]:
                if party_y == self.NOT_COUNTED:
                    vy = final_result_y.summary_statistics.not_counted
                else:
                    vy = othered_d_y.get(
                        party_y,
                        0,
                    )
                py = vy / total
                p = px * py
                # p = p * (1 ** (random.random() - 0.5))
                v.append(p)
        return v

    @cache
    def get_bounds(self):
        X, Y, sample_weight = self.default_training_data
        dimx = len(X[0])
        dimy = len(Y[0])
        bounds = []
        for i in range(dimx * dimy):
            bounds.append((0, 1))
        return bounds

    def get_error_etc(self, v):
        X, Y, sample_weight = self.default_training_data
        n = len(X)
        dimx = len(X[0])
        dimy = len(Y[0])

        dv = [0] * (dimx * dimy)

        error = 0
        weight_sum = 0 
        for i in range(n):
            x = X[i]
            y = Y[i]
            total = sum(y)
            weight = sample_weight[i]
            

            for ix in range(dimx):
                vsum = 0
                for iy in range(dimy):
                    vsum += v[ix * dimy + iy]
                xhat = vsum * total
                dx =  (xhat - x[ix]) 
                error += dx * dx * weight
                weight_sum += weight

                for iy in range(dimy):
                    dv[ix * dimy + iy] -= dx /  (total * weight)

            for iy in range(dimy):
                vsum = 0
                for ix in range(dimx):
                    vsum += v[ix * dimy + iy]
                yhat = vsum * total
                dy = (yhat - y[iy]) 
                error += dy * dy * weight
                weight_sum += weight

                for ix in range(dimx):
                    dv[ix * dimy + iy] -= dx /  (total * weight)

        error = error / weight_sum
        log_error = math.log(error)
        print(f'\log_error={log_error:.8f}', end='\r')

        v_new = [v[i] + dv[i] for i in range(len(v))]
        return error,v_new 

    def get_error(self, v):
        return self.get_error_etc(v)[0]

    @cached_property
    def v_gradient_descent(self):
        v = self.build_init_v()
        for i in range(1_000):
            _, v = self.get_error_etc(v)
        return v

    @cached_property
    def v_scipy(self):
        v = self.build_init_v()
        return minimize(
            self.get_error,
            v,
            method='nelder-mead',
            bounds=self.get_bounds(),
            options=dict(maxiter=10_000,xatol=1e-8,disp=True),
        ).x
    
    @cached_property 
    def v_dummy(self):
        X, Y, _ = self.default_training_data
        n = len(X)
        dimx = len(X[0])
        dimy = len(Y[0])
        v = [0] * (dimx * dimy)
        for i in range(n):
            x = X[i]
            y = Y[i]
            total = sum(y)
            for ix in range(dimx):
                for iy in range(dimy):
                    v[ix * dimy + iy] += x[ix] * y[iy] / total

        sum_v = sum(v)
        return [v[i] / sum_v for i in range(len(v))]


    @cached_property
    def matrix_optimizer(self):
        v = self.v_dummy
        matrix = {}
        i = 0
        total = (
            self.election_x.country_final_result.summary_statistics.electors
        )

        for party_x in self.election_x.get_popular_parties(self.P_LIMIT) + [
            self.NOT_COUNTED
        ]:
            matrix[party_x] = {}
            for party_y in self.election_y.get_popular_parties(
                self.P_LIMIT
            ) + [self.NOT_COUNTED]:
                matrix[party_x][party_y] = v[i] * total
                i += 1
        return matrix
