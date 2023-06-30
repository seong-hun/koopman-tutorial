import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

K1 = 1
K2 = 1
k1 = -1  # mu
k2 = 1  # lambda


def u(x):
    x1, x2 = x
    return -K1 * x1 - K2 * x2


def nonlinear_system(t, x):
    x1, x2 = x
    x1_dot = k1 * x1
    x2_dot = k2 * x2 - k2 * x1**2 + u(x)
    return np.array([x1_dot, x2_dot])


def koopman_linear_system(t, z):
    x = z[:2]
    A = np.array(([k1, 0, 0], [0, k2, -k2], [0, 0, 2 * k1]))
    B = np.array([0, 1, 0])
    z_dot = A @ z + B * u(x)
    return z_dot


fig = plt.figure()
ax = fig.add_subplot(projection="3d", computed_zorder=False)

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(0, 25)
ax.view_init(23, -118)
ax.set_axis_off()

t_span = (0, 50)
t_eval = np.linspace(*t_span, 5000)

data = {"nonlinear_system": {}, "koopman_linear_system": {}}


def set_solution(data, sol):
    data["time"] = sol.t
    data["traj"] = sol.y


set_solution(
    data=data["nonlinear_system"],
    sol=solve_ivp(nonlinear_system, t_span=t_span, y0=(-5, 5), t_eval=t_eval),
)
set_solution(
    data=data["koopman_linear_system"],
    sol=solve_ivp(koopman_linear_system, t_span=t_span, y0=(-5, 5, 25), t_eval=t_eval),
)


class Trajectory:
    def __init__(self, color="k"):
        (self.line,) = ax.plot([], [], [], color=color, zorder=4)
        self.head = ax.scatter([], [], [], marker="o", color=color, zorder=4)
        self.artists = [self.line, self.head]

    def set_data(self, traj_data):
        # traj_data: (3, N)
        self.line.set_data_3d(*traj_data)
        self.head._offsets3d = traj_data[:, -1][:, None]


class ProjectionLine:
    def __init__(self, start=np.zeros(3), end=np.zeros(3), **kwargs):
        data = np.vstack((start, end))
        self.artists = (self.line,) = ax.plot(
            *data.T, **dict(linestyle="--", color="k", zorder=4) | kwargs
        )

    def set_data(self, start, end):
        data = np.vstack((start, end))
        self.line.set_data_3d(*data.T)


class Surface:
    def __init__(self, X, Y, Z, **kwargs):
        self.artists = [
            ax.plot_surface(
                X, Y, Z, **dict(facecolor="w", edgecolor="k", zorder=1) | kwargs
            )
        ]


X, Y = np.meshgrid((-6, 5), (-6, 6))
plane = Surface(X, Y, X * 0)

X, Y = np.meshgrid(np.linspace(-6, 4, 50), np.linspace(-6, 6, 50))
koopman_surface = Surface(X, Y, X**2, facecolor="g", linewidth=0, alpha=0.5)

nonlinear_traj = Trajectory("r")
koopman_traj = Trajectory("b")
proj_line = ProjectionLine()

artists = (
    plane.artists
    + koopman_surface.artists
    + nonlinear_traj.artists
    + koopman_traj.artists
    + proj_line.artists
)


def init():
    return artists


def update(i):
    nonlinear_traj.set_data(
        np.pad(data["nonlinear_system"]["traj"][:, : i + 1], ((0, 1), (0, 0)))
    )
    koopman_traj.set_data(data["koopman_linear_system"]["traj"][:, : i + 1])
    proj_line.set_data(
        start=np.hstack((data["nonlinear_system"]["traj"][:, i], 0)),
        end=data["koopman_linear_system"]["traj"][:, i],
    )
    if i % 20 == 0:
        ProjectionLine(
            linestyle=":",
            start=np.hstack((data["nonlinear_system"]["traj"][:, i], 0)),
            end=data["koopman_linear_system"]["traj"][:, i],
        )

    return artists


ani = animation.FuncAnimation(fig, func=update, init_func=init, frames=400, interval=20)
plt.show()
