from datetime import datetime

class Std:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def n(self):
        return len(self.x)

    @property
    def x_mean(self):
        return sum(self.x) / self.n

    @property
    def y_mean(self):
        return sum(self.y) / self.n

    @property
    def x_variance(self):
        return sum((xi - self.x_mean)**2 for xi in self.x) / self.n

    @property
    def x_q_variance(self):
        return sum((xi - self.x_mean)**2 for xi in self.x) / (self.n - 1)

    @property
    def y_variance(self):
        return sum((yi - self.y_mean)**2 for yi in self.y) / self.n

    @property
    def y_q_variance(self):
        return sum((yi - self.y_mean)**2 for yi in self.y) / (self.n - 1)

    @property
    def covariance(self):
        return sum(map(lambda xi, yi: (xi - self.x_mean) * (yi - self.y_mean), self.x, self.y)) / self.n

    @property
    def gradient(self):
        x_sum = sum(self.x)
        y_sum = sum(self.y)
        numerator = self.n * sum(x * y for x, y in zip(self.x, self.y)) - (x_sum * y_sum)
        denominator = (self.n * sum(x**2 for x in self.x)) - x_sum**2
        return numerator / denominator

    @property
    def interception(self):
        return self.y_mean - self.gradient * self.x_mean

    @property
    def r(self):
        return  self.covariance / ((self.x_variance ** 0.5) * (self.y_variance ** 0.5))

    @property
    def linear_predictions(self):
        return tuple(self.linear_predict(x) for x in self.x)

    def linear_predict(self, x):
        return self.gradient * x + self.interception

    def psc_variance(self, other):
        """Pooled standard deviation of two samples"""

        numerator = ((self.n - 1) * self.y_variance + (other.n - 1) * other.y_variance)
        denominator = self.n + other.n - 2
        return (numerator / denominator) ** 0.5

    def dof(self, other):
        """Degrees of freedom"""

        return self.n + other.n - 2

    def t_statistic(self, other):

        if 0.5 < self.y_variance / other.y_variance < 2:
            return (self.y_mean - other.y_mean) / (self.psc_variance(other) * (1 / self.n + 1 / other.n) ** 0.5)
        else:
            # see https://en.wikipedia.org/wiki/Student%27s_t-test#Equal_variances
            return None

    def __str__(self):
        return f'x: {self.x}\ny: {self.y}\nn: {self.n}'