# Koopman Operator Tutorial

A tutorial for using Koopman operator for controller design.

![ezgif com-video-to-gif](https://github.com/seong-hun/koopman-tutorial/assets/9782545/640ea8af-3d86-4db0-a50d-8c07b5bdb558)

*Source: (Youtube) Steven Brunton's [Koopman Operator Optimal Control](https://www.youtube.com/watch?v=qOdwRel-1xA&t=69s)*

## Requirements

- [Python](https://www.python.org) >= 3.8
- [NumPy](https://numpy.org)
- [Matplotlib](https://matplotlib.org)
- [SciPy](https://scipy.org)

## How to run?

```bash
python main.py
```

## Description

* Nonline system:
```math
\frac{d}{dt} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} k_1 & 0 \\ 0 & k_2 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} + \begin{bmatrix} 0 \\ - k_2 x_1^2 \end{bmatrix} + \begin{bmatrix} 0 \\ 1 \end{bmatrix} u
```

* Control law: $u = - K_1 x_1 - K_2 x_2$

* Koopman lifting: $z = [x_1, x_2, x_1^2]^T$
