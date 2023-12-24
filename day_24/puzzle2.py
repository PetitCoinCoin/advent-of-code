# Failed to use only built-in packages for this one
import sympy as sp
from sympy import solve

if __name__ == "__main__":
    # Took 3 first hailstones data to build a system of 9 equations with 9 variables
    x, y, z, t1, t2, t3, vx, vy, vz = sp.symbols('x, y, z, t1, t2, t3, vx, vy, vz')
    eq1 = sp.Eq(z + vz * t1 - 262795384692232 - 39 * t1, 0)
    eq2 = sp.Eq(y + vy * t1 - 401088290781515 + 36 * t1, 0)
    eq3 = sp.Eq(x + vx * t1 - 189484959431670 - 95 * t1, 0)
    eq4 = sp.Eq(z + vz * t2 - 297355219841654 + 56 * t2, 0)
    eq5 = sp.Eq(y + vy * t2 - 163094456512341 - 182 * t2, 0)
    eq6 = sp.Eq(x + vx * t2 - 175716591307178 - 160 * t2, 0)
    eq7 = sp.Eq(z + vz * t3 - 314435988531407 + 10 * t3, 0)
    eq8 = sp.Eq(y + vy * t3 - 363632912812075 - 37 * t3, 0)
    eq9 = sp.Eq(x + vx * t3 - 283402568811320 + 6 * t3, 0)
    output = solve([eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9], x, y, z, t1, t2, t3, vx, vy, vz, dict=True)
    print(output[0][x] + output[0][y] + output[0][z])
