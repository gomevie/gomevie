import random
from sympy import sympify
from sympy import sympify, Rational
from fractions import Fraction
import argparse

# 初始化argparse对象
parser = argparse.ArgumentParser(description="处理命令行参数")


operate = {
    '+': '+',
    '-': '-',
    '*': 'x',
    '/': '÷'
}


def save_data(data, filename_expressions, filename_results):
    with open(filename_expressions, 'w') as f_expressions, open(filename_results, 'w') as f_results:
        for expression, result in data:
            f_expressions.write(f"{expression}\n")
            f_results.write(f"{result}\n")


def calculate_expression(expression):
    try:
        # 使用sympify函数解析和计算表达式
        result = sympify(expression).evalf()
        # 如果结果是一个整数，就转换为整数分数形式
        if result == int(result):
            result_fraction = str(int(result))
        else:
            # 如果结果不是整数，就转换为分数形式
            result_fraction = Fraction(str(result)).limit_denominator()
            # 分子和分母
            numerator, denominator = int(result_fraction.numerator), int(result_fraction.denominator)
            if numerator > denominator:
                # 分子大于分母，转换为带分数形式
                result_fraction = f"{numerator // denominator}'{numerator % denominator}/{denominator}"

        return str(result_fraction)

    except Exception as e:
        # 如果发生错误，返回错误信息
        return f"Error: {e}"


# 检查表达式是否为真分数
def is_true_fraction(expr, max_value):
    try:
        result = sympify(expr).evalf()
        return max_value > result >= 0
    except:
        return False


# 检查表达式是否有效
def is_valid_expression(expr):
    try:
        result = sympify(expr).evalf()
        return result >= 0 and expr.count('+') + expr.count('-') + expr.count('*') + expr.count('/') <= 3
    except:
        return False


# 生成真分数
def generate_true_fraction(max_value):
    num = random.randint(1, max_value)
    den = random.randint(1, min(max_value, 20))
    while num >= den:  # 确保分数为真分数
        return f"{num // den}"
    return f"{num}/{den}"


# 生成四则运算题目
def generate_expressions(max_value, count):
    expressions = set()
    while len(expressions) < count:
        # 生成运算符，确保不会产生负数
        operators = random.sample(['+', '-', '*', '/'], random.randint(1, 3))

        fraction1 = generate_true_fraction(max_value)
        expr = f"{fraction1}"
        expr_true = f"{fraction1}"

        # 构建表达式
        for i, op in enumerate(operators):

            fraction2 = generate_true_fraction(max_value)
            expr += f"{operate[op]}{fraction2}"
            expr_true += f"{op}{fraction2}"


            # 随机添加括号
            if random.choice([True, False]) and len(operators)-1 != i:
                expr = f"({expr})"
        if is_valid_expression(expr_true) and is_true_fraction(expr_true, max_value):
            expressions.add((expr+' =', calculate_expression(expr_true)))

    return expressions


# 主程序
def main(max_value=100, count=100):
    if max_value < 1 or count <= 0:
        raise ValueError("参数必须是给定的自然数。")

    expressions = generate_expressions(max_value, count)
    save_data(expressions, "Exercises.txt", "Answers.txt")
    for expr in expressions:
        print(f"{expr}")


# 读取文件中的答案
def read_answers(filename):
    try:
        with open(filename, 'r') as file:
            answers = [line.strip() for line in file.readlines()]
        return answers
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 '{filename}' 不存在。")


# 检查答案是否相同
def compare_answers(correct, student):
    correct_count = sum(1 for c, s in zip(correct, student) if c == s)
    wrong_count = len(student) - correct_count
    return correct_count, wrong_count


# 将统计结果写入文件
def write_grades_to_file(correct_count, wrong_count, correct_list, wrong_list, output_file):
    with open(output_file, 'w') as file:
        file.write(f"Correct: {correct_count}({', '.join(map(str, correct_list))})\n")
        file.write(f"Wrong: {wrong_count}({', '.join(map(str, wrong_list))})\n")


def calculate_grades(correct_answers_file, student_answers_file, output_file):
    # 读取正确答案和学生答案
    correct_answers = read_answers(correct_answers_file)
    student_answers = read_answers(student_answers_file)

    # 检查答案数量是否相同
    if len(correct_answers) != len(student_answers):
        raise ValueError("答案数量不相同，无法进行比较。")

    # 比较答案并获取正确和错误的列表
    correct_count, wrong_count = compare_answers(correct_answers, student_answers)
    correct_list = [index + 1 for index, (c, s) in enumerate(zip(correct_answers, student_answers)) if c == s]
    wrong_list = [index + 1 for index, (c, s) in enumerate(zip(correct_answers, student_answers)) if c != s]

    # 写入文件
    write_grades_to_file(correct_count, wrong_count, correct_list, wrong_list, output_file)


if __name__ == "__main__":
    # 添加参数
    parser.add_argument('-n', type=int, default=100, help='输入题目数量')
    parser.add_argument('-r', type=int, default=-1, help='输入运算最大值')
    parser.add_argument('-e', default=-1, help='输入所作答案文件的名称')
    parser.add_argument('-a', default=-1, help='输入真实答案文件的名称')
    parser.add_argument('-o', default='Grade.txt', help='统计结果文件的名称')

    # 解析命令行参数
    args = parser.parse_args()

    if args.a == -1 and args.e == -1:
        if args.r == -1:
            raise ValueError("运算最大值必须是给定的自然数。")
        main(args.n, args.r)

    else:
        if args.a == -1 or args.e == -1:
            raise ValueError("所作答案文件与真实答案文件必须同时存在。")

        else:
            calculate_grades(args.a, args.e, args.o)
