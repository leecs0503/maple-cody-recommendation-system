import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

NUM_TEST = 50
NUM_CODE = 15

with open('json_data_result_1_3000.json', encoding='utf-8') as file:
    json_data = json.load(file)

res_list = []
code_dic = {'face': [], 'cap': [], 'longcoat': [], 'weapon': [], 'cape': [], 'coat': [], 'glove': [], 'hair': [], 'pants': [], 'shield': [], 'shoes': [], 'faceAccessory': [], 'eyeAccessory': [], 'earrings': [], 'skin': []}

for k, v in json_data.items():
    for recent_cody_num in range(len(json_data[k])):
        temp_list = []
        for recent_cody_num_key, recent_cody_num_value in json_data[k][recent_cody_num].items():
            if '+' in recent_cody_num_value:
                recent_cody_num_value = recent_cody_num_value.split('+')
                temp_list.append(recent_cody_num_value[0])
                code_dic[recent_cody_num_key] += [recent_cody_num_value[0]]
                continue

            temp_list.append(recent_cody_num_value)
            code_dic[recent_cody_num_key] += [recent_cody_num_value]

        res_list.append(temp_list)


res_string_list = []
idx_list = []
total_acc = 0

for idx, data in enumerate(res_list):
    string = f'{data[0]} {data[1]} {data[2]} {data[3]} {data[4]} {data[5]} {data[6]} {data[7]} {data[8]} {data[9]} {data[10]} {data[11]} {data[12]} {data[13]} {data[14]}'
    res_string_list.append(string)
    idx_list.append((idx, string))

for count in range(NUM_TEST):
    test_list = []
    for k, v in code_dic.items():
        # code_dic[k] = list(set(code_dic[k])) 중복 제거 할 때
        random_sample_num = random.choice(code_dic[k])
        test_list.append(random_sample_num)

    test = f'{test_list[0]} {test_list[1]} {test_list[2]} {test_list[3]} {test_list[4]} {test_list[5]} {test_list[6]} {test_list[7]} {test_list[8]} {test_list[9]} {test_list[10]} {test_list[11]} {test_list[12]} {test_list[13]} {test_list[14]}'
    res_string_list.append(test)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(res_string_list)
    # print('TF-IDF 행렬의 크기(shape) :',tfidf_matrix.shape)

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    test_idx = cosine_sim.shape[0] - 1

    sim_scores = list(enumerate(cosine_sim[test_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    avatar_indices = sim_scores[1][0]
    res_code = idx_list[avatar_indices][1]

    split_test = test.split(' ')
    split_res_code = res_code.split(' ')

    cnt = 0
    for i in range(NUM_CODE):
        if test[i] == res_code[i]:
            cnt += 1

    acc = cnt / NUM_CODE
    print(f'{count+1}\'st acc : ', acc)
    total_acc += acc
    res_string_list.pop()

total_acc = total_acc / NUM_TEST
print("total_acc : ", total_acc)
