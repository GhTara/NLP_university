import difflib
import pandas as pd
from hazm import *
import re


def read_save_result(result, tokenizer_name):

    print(result)
    col_name = tokenizer_name + '_re'
    df = pd.DataFrame({col_name: result})
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    file_out_name = tokenizer_name + '.xlsx'
    writer = pd.ExcelWriter(file_out_name, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


normalizer = Normalizer()


col_name = "parsipardaz"
df = pd.read_excel("parsipardaz.xlsx", sheet_name='Sheet1')
# print(len(df["main"].values))
parsivarS = list(df[col_name].values)
parsivarS = ['='.join(sen.split(' ')) for sen in parsivarS]

col_name = "hand_made"
df = pd.read_excel("Tokenizer.xlsx", sheet_name='Sheet1')
# print(len(df["main"].values))
hand_madeS = df[col_name].values
# print(hand_madeS[0])

is_same = []
true_token = []
test_token = []
diff_comp_num = []
total_comp = []
for i in range(156):

    parsivar = normalizer.normalize(parsivarS[i])
    hand_made = normalizer.normalize(hand_madeS[i].strip(' '))
    # print(i)
    # print(hand_made)
    # parsivar = 'او=بسیار=پسر=با=ادبی=است=.'

    # hand_made = hand_made.replace('÷', ' ')
    # hand_made = hand_made.replace('\u200c', ' ')
    # parsivar = parsivar.replace('\u200c', ' ')
    count_H = len(hand_made.split('='))

    set1 = [re.sub(r'\u200c+', '\u200c', x.strip().replace(' ', '\u200c'))
            for x in hand_made.split('=')]
    comp_total = []
    for j, s in enumerate(set1):
        if '÷' in s:
            comp = [w.strip() for w in s.split('÷')]
            comp = '\u200c'.join(comp)
            comp_total.append(comp)
            if i == 58:
                print(comp)
            set1[j] = comp

    true_token.append(len(set1))
    set2 = [re.sub(r'\u200c+', '\u200c', x.strip().replace(' ', '\u200c'))
            for x in parsivar.split('=')]

    diff_label = diff(set1, set2)
    total = len(set1)
    diff_label_num = len(diff_label)
    test_token.append(total - diff_label_num)
    # if i == 120:
    #     print(total - diff_label_num)

    if diff_label_num == 0:
        is_same.append(1)
    else:
        is_same.append(0)

    if(i == 58):
        print((set1))
        print((set2))
        print(len(set1))
        print(len(set2))
        # print(set(set1)-set(set2))
        print('='.join(diff_label))
        # print(len(set1-set2))

    diff_comp_num.append(len(comp_total) - len(diff(comp_total, set2)))
    total_comp.append(len(comp_total))

read_save_result(is_same, 'is_same')
# read_save_result(true_token, '#total_token')
# read_save_result(test_token, '#token_reconized')
read_save_result(test_token, '#token_reconized')
read_save_result(diff_comp_num, '#compound_words_true')
# read_save_result(total_comp, '#compound_words_total')


# print(test_token[47])
# print(hand_madeS[47].strip('='))


# parsivar = 'او=بسیار=پسر=با=ادبی=است=.'
# count_P = len(parsivar.split('='))

# print(count_H+1)
# print(count_P+1)
