# import functools

# logged_in = False


# def is_logged_in(func):
#     @functools.wraps(func)
#     def func_wrapper(*args, **kwargs):
#         if logged_in:
#             return func(*args, **kwargs)
#         else:
#             print("Please login to perform this action.")

#     return func_wrapper


# def print_func_name(func):
#     @functools.wraps(func)
#     def func_wrapper(*args, **kwargs):
#         print("function name: ", func.__name__)

#         return func(*args, **kwargs)

#     return func_wrapper


# @print_func_name
# @is_logged_in
# def print_users():
#     print("Mike, Mark, Royeal, Sarah")


# print_users()

# def add_nums(function):
#     def function_wrapper(*args, **kwargs):
#         sum_1 = args[0] + args[1]
#         sum_2 = args[2] + args[3]

#         kwargs["sum_1"] = sum_1
#         kwargs["sum_2"] = sum_2

#         print("function_name: ", function.__name__)

#         return function(*args, **kwargs)
#     return function_wrapper


# @add_nums
# def multiply_sum(num_1, num_2, num_3, num_4, sum_1=1, sum_2=1):
#     return sum_1 * sum_2


# @add_nums
# def divide_sum(num_1, num_2, num_3, num_4, sum_1=1, sum_2=1):
#     return sum_1 / sum_2


# print(multiply_sum(1, 2, 3, 4))
# print(divide_sum(1, 2, 3, 4))


# @custom_decorator_name
# def print_favorite_color(favorite_color, least_favorite_color, default_favorite="purple"):
#     print(f"My favorite color is {favorite_color}")
#     print(f"My least favorite color is {least_favorite_color}")
#     print(f'My default favorite color is {default_favorite}')


# @custom_decorator_name
# def print_favorite_food(favorite_food, least_favorite_food, default_favorite="corn"):
#     print(f'My favorite food is {favorite_food}')
#     print(f"My least favorite food is {least_favorite_food}")
#     print(f"My default favorite food is {default_favorite}")


# print_favorite_food("pizza", "saurkraut", default_favorite="apples")
# print_favorite_color("orange", "black", default_favorite="yello")


# def print_args_kwargs(*args, **kwargs):
#     print(args)
#     print(kwargs)


# print_args_kwargs(3, 2, 1, 5, 6, 7, first_name="Mark", last_name="Hill")


import functools


def print_args(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        print(func.__name__)
        for idx, e in enumerate(args):
            print(f'{idx}: {e}')
        return func(*args, **kwargs)
    return decorator_wrapper


@print_args
def sum_num(*args):
    return sum(list(args))


@print_args
def concatenate_str(*args):
    return " ".join(args)


@print_args
def sort_list(*args):
    return sorted(list(args))


print(sum_num(1, 2, 3))
print(concatenate_str("hello", "world"))
print(sort_list(32, 14, 27, 60))
