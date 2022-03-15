import json

with open('/home/datasets/VizWiz/Annotations/test.json', 'r') as f:
    labels = json.load(f)

with open('../results20220214/best-15/test2015_results.json', 'r') as f:
    oscar_results = json.load(f)

outputs = []
for i, result in enumerate(oscar_results):
    q_id = result['question_id']
    answer = result['answer']
    unit = {
            'image':labels[i]['image'],
            'answer':answer
            }
    # print(unit)
    # break
    outputs.append(unit)

with open("results.json", 'w') as f:
    json.dump(outputs, f)


