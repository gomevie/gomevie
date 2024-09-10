import pstats

# 创建一个 Stats 对象并加载剖析结果
p = pstats.Stats('profiling_results.stats')

# 按照累计时间排序并打印详细信息
p.strip_dirs().sort_stats('cumtime').print_stats(10)