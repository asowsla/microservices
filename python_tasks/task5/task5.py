import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f"Время выполнения: {elapsed:.7f} сек")
        return result
    return wrapper

@timer
def sum(a, b):
    result = a + b
    print("sum: ", result)
    return result

@timer
def file_sum():
    with open("input.txt", "r") as input_file:
        numbers = tuple(map(int, input_file.read().split()))
    
    sum_result = numbers[0] + numbers[1]

    with open("output.txt", "w") as output_file:
        output_file.write(str(sum_result))

    print("sum: ", sum_result)

def main():

    print("sum() result:")
    sum(-190, 3)

    print("\nfile_sum() result:")
    file_sum()


if __name__ == "__main__":      
    main()