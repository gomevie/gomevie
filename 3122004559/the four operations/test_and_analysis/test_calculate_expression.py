# coding=utf-8

from Myapp import calculate_expression



def test_calculate_expression():
    # 正常表达式，结果为整数
    assert calculate_expression("2+2") == "4"
    assert calculate_expression("299+201") == "500"

    # 正常表达式，结果为分数
    assert calculate_expression("1/2 + 1/3") == "5/6"
    assert calculate_expression("1/18 + 2/9") == "5/18"

    # 正常表达式，结果为带分数
    assert calculate_expression("3+2/3") == "3'2/3"
    assert calculate_expression("1/2+2/3") == "1'1/6"

    # 含错误的表达式
    assert calculate_expression("a+b").startswith("Error:")
    assert calculate_expression("2 + /3").startswith("Error:")


if __name__ == "__main__":
    test_calculate_expression()

