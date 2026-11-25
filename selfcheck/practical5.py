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


ROCKET = dict(g=9.81, thrust=4000.0, Isp=220.0, m0=100.0, m_dry=40.0, Cd=0.5,
              A=np.pi * 0.1**2, rho0=1.225, H=8500.0)


def _rocket_derivatives(state, p):
    h, v, m = state
    if m > p["m_dry"]:
        T, dm = p["thrust"], -p["thrust"] / (p["Isp"] * p["g"])
    else:
        T, dm = 0.0, 0.0
    D = 0.5 * p["rho0"] * np.exp(-h / p["H"]) * p["Cd"] * p["A"] * v * abs(v)
    return [v, (T - m * p["g"] - D) / m, dm]


def exercise3():
    """Exercise 3: vertical launch of a sounding rocket with fuel burn and drag."""
    from scipy.integrate import odeint

    with Checker("Practical 5, Exercise 3") as c:
        func = c.need("rocket_equations")
        p = dict(ROCKET)
        changed = [k for k in p if k in c.ns and not np.isclose(c.ns[k], p[k])]
        if changed:
            c.fail(f"These parameters are different from the template: {', '.join(changed)}.",
                   "The checks use the template values. Change them back, re-run the exercise cell, "
                   "then try the questions once the checks pass.")
            c.stop()

        def call(state):
            try:
                return [float(x) for x in func(list(state), 0.0)]
            except Exception as exc:  # noqa: BLE001
                c.fail(f"`rocket_equations` crashed: {type(exc).__name__}: {exc}",
                       "Take h = array[0], v = array[1] and m = array[2] first, and make sure "
                       "dh_dt, dv_dt and dm_dt all get a value.")
                c.stop()

        launch = call([0.0, 0.0, 100.0])           # on the pad, full of fuel
        climbing = call([5000.0, 300.0, 70.0])     # burning, moving fast through the air
        coasting = call([20000.0, 500.0, 40.0])    # fuel used up
        falling = call([40000.0, -300.0, 40.0])    # coming back down

        c.check(np.isclose(climbing[0], 300.0) and np.isclose(falling[0], -300.0),
                "dh/dt = v is correct", "dh/dt is not right yet.", "The rate of change of height is just the velocity: dh_dt = v")
        c.check(np.isclose(launch[2], -4000.0 / (220.0 * 9.81)) and np.isclose(coasting[2], 0.0),
                "The mass falls while the engine burns, then stays constant",
                "dm/dt is not right yet.",
                "Inside the if (m > m_dry): dm_dt = -thrust / (Isp * g). In the else part: dm_dt = 0.0")
        c.check(np.isclose(launch[1], (4000.0 - 100.0 * 9.81) / 100.0),
                "dv/dt at launch is correct (thrust minus weight, no drag yet)",
                "dv/dt at launch is not right yet.",
                "At launch v = 0, so there is no drag: dv_dt = (T - m*g - D) / m with T = thrust.")
        exp_coast = _rocket_derivatives([20000.0, 500.0, 40.0], p)[1]
        if not np.isclose(coasting[1], exp_coast, rtol=1e-4):
            if np.isclose(coasting[1], (4000.0 - 40.0 * 9.81 - 0.5 * 1.225 * np.exp(-20000 / 8500) * 0.5 * p["A"] * 500**2) / 40.0, rtol=1e-4):
                c.fail("The engine keeps burning after the fuel has run out.",
                       "Set T = 0.0 in the else part of your if statement.")
            else:
                c.fail("dv/dt is not right once the fuel has run out.",
                       "Check the drag: D = 0.5 * rho * Cd * A * v * abs(v), with rho = rho0 * np.exp(-h / H).")
        else:
            c.ok("The engine switches off when the fuel runs out")
        exp_fall = _rocket_derivatives([40000.0, -300.0, 40.0], p)[1]
        if np.isclose(falling[1], exp_fall, rtol=1e-4):
            c.ok("Drag acts against the motion, both going up and coming down")
        else:
            wrong = -9.81 - 0.5 * 1.225 * np.exp(-40000 / 8500) * 0.5 * p["A"] * 300**2 / 40.0
            c.fail("dv/dt is not right while the rocket is falling.",
                   "Use v * abs(v) in the drag, not v**2, so that drag pushes upwards on the way down."
                   if np.isclose(falling[1], wrong, rtol=1e-4) else
                   "Check the drag: D = 0.5 * rho * Cd * A * v * abs(v), with rho = rho0 * np.exp(-h / H).")

        t = np.array(c.need("t"), dtype=float)
        solution = np.array(c.need("solution"), dtype=float)
        expected = odeint(lambda s, _t: _rocket_derivatives(s, p), (0.0, 0.0, 100.0), t)
        if solution.shape != expected.shape:
            c.fail(f"`solution` has shape {solution.shape}, but it should have shape {expected.shape}.",
                   "Call odeint(rocket_equations, (0.0, 0.0, m0), t): three starting values, height, velocity and mass.")
        else:
            c.check(np.allclose(solution, expected, rtol=1e-3, atol=1e-2),
                    f"`solution` is correct: the apogee is {expected[:, 0].max() / 1000:.1f} km",
                    "`solution` does not match the expected flight.",
                    "Start on the ground, at rest and full of fuel: odeint(rocket_equations, (0.0, 0.0, m0), t)")
