# Chap 2. 프로파일링으로 병목 지점 찾기

## 시간을 측정하는 여러가지 방법

1. 가장 간단한 `print` 문 사용하기

2. 데커레이터 사용하기

```python3
from functools import wraps

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {fn.__name__} took {t2 - t1} seconds")
        return result
    return measure_time

@timefn
def calculate_z_serial_purepython(maxiter, zs, cs):
    ...
```
3. `timeit` 모듈을 사용하여 CPU를 집중적으로 사용하는 함수의 실행 속도 측정하기
```shell
$ python -m timeit -n 5 -r 1 -s "import julia_set" \
"julia_set.calc_pure_python(desired_width=1000, max_iterations=300)"
```
- -s: 모듈 임포트
- -r: 반복 횟수
- -n: 반복당 시간 측정 횟수
4. 유닉스 `time` 명령어를 이용하기
```shell
$ /usr/bin/time -p python julia_set.py
```
- `Major (requiring I/O) page faults`: 운영체제가 RAM에서 필요한 데이터를 찾을 수 없기 때문에 디스크에서 페이지를 불러왔는지 여부. -> 속도를 느리게 하는 원인
5. `cProfile` 모듈 사용하기
```shell
$ python -m cProfile -s cumulative julia_set.py
```
- `-s cumulative`: 각 함수에서 소비한 누적 시간순으로 정렬하여 어떤 함수가 느린지 쉽게 확인 가능
- 통계 파일 생성한 후 파이썬으로 좀 더 상세한 분석하기
```shell
$ python -m cProfile -o profile.stats julia_set.py
```
```python3
import pstats
p = pstats.Stats("profile.stats")
p.sort_stats("cumulative")
p.print_stats()
```
6. `line_profiler`로 한 줄씩 측정하기
```shell
$ kernprof -l -v julia_line_profile.py
```
7. `py-spy'로 측정하기
```shell
$ python julia_set.py # 미리 실행
```
```shell
ps -A | grep python
```
```shell
$ sudo env "PATH=$PATH" py-spy top --pid {pid}
```