# coding=utf-8
import cProfile
import pstats
from Myapp import main

# 创建一个分析器对象
profiler = cProfile.Profile()
# 开始分析
profiler.enable()
main()
# 停止分析
profiler.disable()

# 创建一个统计对象并流式传输数据到控制台
stats = pstats.Stats(profiler).sort_stats('cumtime')
stats.print_stats()

# 将分析结果写入文件
profiler.dump_stats('profile_stats.prof')