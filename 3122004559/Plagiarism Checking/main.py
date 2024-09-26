import sys
import os
import jieba
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 读取文件内容
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        sys.exit(1)
    except IOError:
        print(f"Error: Cannot read file {file_path}.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


# 使用jieba进行中文分词
def tokenize(text):
    try:
        return list(jieba.cut(text))
    except Exception as e:
        print(f"Error during tokenization: {e}")
        sys.exit(1)

# 计算原文和抄袭版的相似度，并输出结果
def calculate_similarity(original_file, plagiarized_file):
    original_text = read_file(original_file)
    plagiarized_text = read_file(plagiarized_file)

    original_tokens = tokenize(original_text)
    plagiarized_tokens = tokenize(plagiarized_text)

    # 将文本转换为TF-IDF向量
    tfidf_vectorizer = TfidfVectorizer()
    original_tfidf = tfidf_vectorizer.fit_transform([' '.join(original_tokens)])
    plagiarized_tfidf = tfidf_vectorizer.transform([' '.join(plagiarized_tokens)])

    # 计算余弦相似度
    cosine_sim = cosine_similarity(original_tfidf, plagiarized_tfidf)

    # 计算相似度百分比
    similarity_percentage = cosine_sim[0, 0] * 100

    return similarity_percentage




def write_output(file_path, similarity):
    # 检查输出文件路径是否存在，不存在则在当前工作目录创建文件
    try:
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f'{similarity:.2f}\n')
    except IOError:
        print(f"Error: Cannot write to file {file_path}.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while writing output: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py [original_file] [plagiarized_file] [output_file]")
        sys.exit(1)

    original_file = sys.argv[1]
    plagiarized_file = sys.argv[2]
    output_file = sys.argv[3]

    similarity = calculate_similarity(original_file, plagiarized_file)
    write_output(output_file, similarity)

