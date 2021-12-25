import time
grid_shape = (640, 640)

# 6-6 메모리 할당을 줄인 순수 파이썬 2차원 확산 방정식 코드
@profile
def evolve(grid, dt, out, D=1.0):
    xmax, ymax = grid_shape
    for i in range(xmax):
        for j in range(ymax):
            grid_xx = (
                grid[(i + 1) % xmax][j] + grid[(i - 1) % xmax][j] - 2.0 * grid[i][j]
            )
            grid_yy = (
                grid[i][(j + 1) % ymax] + grid[i][(j - 1) % ymax] - 2.0 * grid[i][j]
            )
            out[i][j] = grid[i][j] + D * (grid_xx + grid_yy) * dt
            
def run_experiment(num_iterations):
    # 초기 조건 설정
    xmax, ymax = grid_shape
    next_grid = [[0.0] * ymax for x in range(xmax)]
    grid = [[0.0] * ymax for x in range(xmax)]

    # 시뮬레이션 영역의 중간에 물감이 한 방울
    # 떨어진 상태를 시뮬레이션하기 위한 초기 조건들
    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    for i in range(block_low, block_high):
        for j in range(block_low, block_high):
            grid[i][j] = 0.005

    # 초기 조건을 변경한다.
    start = time.time()
    for i in range(num_iterations):
        evolve(grid, 0.1, next_grid)
        grid, next_grid = next_grid, grid
    return time.time() - start

if __name__ == "__main__":
    run_experiment(50)
    """
$kernprof -lv chap06/diffusion_python.py
Wrote profile results to diffusion_python.py.lprof
Timer unit: 1e-06 s

Total time: 78.1584 s
File: chap06/diffusion_python.py
Function: evolve at line 5

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     5                                           @profile
     6                                           def evolve(grid, dt, D=1.0):
     7        50        124.0      2.5      0.0      xmax, ymax = grid_shape
     8        50      19625.0    392.5      0.0      new_grid = [[0.0] * ymax for x in range(xmax)]
     9     32050      14448.0      0.5      0.0      for i in range(xmax):
    10  20512000    9124381.0      0.4     11.7          for j in range(ymax):
    11  20480000    9220234.0      0.5     11.8              grid_xx = (
    12  20480000   18100608.0      0.9     23.2                  grid[(i + 1) % xmax][j] + grid[(i - 1) % xmax][j] - 2.0 * grid[i][j]
    13                                                       )
    14  20480000    8896408.0      0.4     11.4              grid_yy = (
    15  20480000   18085316.0      0.9     23.1                  grid[i][(j + 1) % ymax] + grid[i][(j - 1) % ymax] - 2.0 * grid[i][j]
    16                                                       )
    17  20480000   14697157.0      0.7     18.8              new_grid[i][j] = grid[i][j] + D * (grid_xx + grid_yy) * dt
    18        50        121.0      2.4      0.0      return new_grid
    """