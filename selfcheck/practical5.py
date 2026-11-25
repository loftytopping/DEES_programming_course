"""Self-checks for Practical 5: solving ordinary differential equations."""

from ._core import Checker, np

GAMMAS = [1.0, 1.5, 2.0, 5.0, 8.0, 12.0, 15.0, 20.0, 22.5, 25.0]


def exercise1():
    """Exercise 1: exponential decay for 10 decay coefficients."""
    t_expected = np.linspace(0, 1, num=100)
    with Checker("Practical 5, Exercise 1") as c:
        t = c.need("t")
        c.sequence("t", t, t_expected, describe_index=lambda i: f"t[{i[0]}]",
                   hints=[(np.linspace(0, 10, num=100), "The time span should run from 0 to 1 second.")])
        store = np.array(c.need("solution_store_array"), dtype=float)
        decay = 1000 * np.exp(-np.outer(t_expected, GAMMAS))
        growth = 1000 * np.exp(np.outer(t_expected, GAMMAS))
        if store.shape == decay.shape and np.allclose(store, growth, rtol=1e-3):
            c.fail("Your curves grow instead of decay.",
                   "For decay the derivative must be negative: return -1.0*Gamma*N in differential_function.")
        elif store.shape == decay.shape and np.allclose(store, 1000 * np.exp(-25.0 * t_expected)[:, None], rtol=1e-3):
            c.fail("All 10 columns use the same decay coefficient.",
                   "Inside the loop, set Gamma = Gamma_array[i] before calling odeint.")
        else:
            c.sequence("solution_store_array", store, decay, rel=1e-3, atol=1e-3,
                       describe_index=lambda i: f"time step {i[0]} for Gamma = {GAMMAS[i[1]]}",
                       hints=[(np.zeros((100, 10)), "The array is still all zeros. Call odeint inside the loop: "
                                                   "solution = odeint(differential_function, No, t)")])


def _lotka_volterra(a, b, c, d, u0, v0, t):
    from scipy.integrate import odeint

    def f(y, _t):
        u, v = y
        return [a * u - b * u * v, -c * v + d * b * u * v]
    return odeint(f, (u0, v0), t)


def exercise2():
    """Exercise 2: the Lotka-Volterra predator-prey model."""
    with Checker("Practical 5, Exercise 2") as c:
        a, b, cc, d = (c.need(n) for n in ("a", "b", "c", "d"))
        u0, v0 = c.need("U0"), c.need("V0")
        func = c.need("differential_equations")
        try:
            du, dv = func([10.0, 5.0], 0.0)
        except Exception as exc:  # noqa: BLE001
            c.fail(f"`differential_equations` crashed: {type(exc).__name__}: {exc}",
                   "Inside the function, take U = array[0] and V = array[1] first.")
            c.stop()
        U, V = 10.0, 5.0
        c.check(np.isclose(du, a * U - b * U * V), "dU/dt = aU - bUV is correct",
                "dU/dt is not right yet.", "dU_dt = a*U - b*U*V")
        c.check(np.isclose(dv, -cc * V + d * b * U * V), "dV/dt = -cV + dbUV is correct",
                "dV/dt is not right yet.", "dV_dt = -c*V + d*b*U*V  (note the minus sign)")

        params = dict(a=1.0, b=0.1, c=1.5, d=0.75, U0=10, V0=5)
        given = dict(a=a, b=b, c=cc, d=d, U0=u0, V0=v0)
        wrong = [k for k in params if not np.isclose(given[k], params[k])]
        c.check(not wrong, "The parameters match the example figure",
                f"These values don't match the figure yet: {', '.join(wrong)}.",
                "Use the values from the Scipy cookbook example linked in the exercise: "
                "a = 1, b = 0.1, c = 1.5, d = 0.75, U0 = 10, V0 = 5.")

        solution = np.array(c.need("solution"), dtype=float)
        t = np.array(c.need("t"), dtype=float)
        expected = _lotka_volterra(a, b, cc, d, u0, v0, t)
        c.sequence("solution", solution, expected, rel=1e-3, atol=1e-3,
                   describe_index=lambda i: f"time step {i[0]} ({'rabbits' if i[1] == 0 else 'foxes'})",
                   hints=[(expected[:, ::-1], "Rabbits and foxes are swapped. Pass the starting values as (U0, V0).")])
