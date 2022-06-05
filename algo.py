import pandas as pd
import numpy as np
import math
import re
from collections import Counter


WORD = re.compile(r"\w+")
regex = re.compile('[^a-zA-Z]')


def match_color(color_list,recommend_desc):
    colors = " ".join(color_list)
    colors = regex.sub(' ', colors)
    cosine_similarity_list_for_acs = []
    for text in recommend_desc:
        text1 = str(text)
        text1 = text1.lower()
        text2 = str(colors)
        text2 = text2.lower()

        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        cosine = get_cosine(vector1, vector2)
        cosine_similarity_list_for_acs.append(cosine)
    text_cosine_dic_for_acs = {}
    patt_ind = 0

    for cos, text in zip(cosine_similarity_list_for_acs, recommend_desc):
        text_cosine_dic_for_acs[cos] = [text, patt_ind]
        patt_ind += 1

    sort_keys = sorted(text_cosine_dic_for_acs.keys(), reverse=True)

    ind = []
    for key in sort_keys:
        if key!=0.0:
            ind.append(text_cosine_dic_for_acs[key][-1])

    return ind

def get_pattern_recommendation(pattern_input,recommend_desc):
    cosine_similarity_list_for_pattren = []
    for text in recommend_desc:
        text1 = str(text)
        text1 = text1.lower()
        text2 = str(pattern_input)
        text2 = text2.lower()

        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        cosine = get_cosine(vector1, vector2)
        cosine_similarity_list_for_pattren.append(cosine)
    
    text_cosine_dic_for_patt = {}
    patt_ind = 0
    for cos, text in zip(cosine_similarity_list_for_pattren, recommend_desc):
        text_cosine_dic_for_patt[cos] = [text, patt_ind]
        patt_ind += 1

    sort_keys = sorted(text_cosine_dic_for_patt.keys(), reverse=True)
    ind = []
    for key in sort_keys:
        if key!=0.0:
            # print(text_cosine_dic_for_patt[key])
            ind.append(text_cosine_dic_for_patt[key][-1])

    return ind
    


def get_materials_recommendation(input_saree, mat_dic,recommend_desc):
    comp_color_list = None
    for key in mat_dic.keys():
        input_saree = input_saree.lower()
        if key==input_saree:
            comp_color_list = mat_dic[key]
    
    recom_mat = " ".join(comp_color_list)
    cosine_similarity_list_for_material = []

    for text in recommend_desc:
        text1 = str(text)
        text1 = text1.lower()
        text2 = str(recom_mat)
        text2 = text2.lower()

        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        cosine = get_cosine(vector1, vector2)
        cosine_similarity_list_for_material.append(cosine)
    
    text_cosine_dic_for_mat = {}
    patt_ind = 0
    for cos, text in zip(cosine_similarity_list_for_material, recommend_desc):
        text_cosine_dic_for_mat[cos] = [text, patt_ind]
        patt_ind += 1

    sort_keys = sorted(text_cosine_dic_for_mat.keys(), reverse=True)

    ind = []
    for key in sort_keys:
        if key!=0.0:
            # print(text_cosine_dic_for_mat[key])
            ind.append(text_cosine_dic_for_mat[key][-1])

    return ind    

def recom_ind(sort_keys, text_cosine_dic):
    ind = []
    for key in sort_keys:
        if key!=0.0:
     #       print(text_cosine_dic[key])
            ind.append(text_cosine_dic[key][-1])
    return ind

def get_text_cosine_dic(cosine_similarity_list, desc_text):
    ind = 0
    text_cosine_dic = {}
    for cos, text in zip(cosine_similarity_list, desc_text):
        text_cosine_dic[cos] = [text, ind]
        ind += 1

    return text_cosine_dic

def text_to_vector(text):
    words = WORD.findall(text)

    return Counter(words)

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def get_cosine_similarity_list(desc_text, recom_colors):
    cosine_similarity_list = []
    for text in desc_text:
        text1 = str(text)
        text1 = text1.lower()
        text2 = str(recom_colors)

        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        cosine = get_cosine(vector1, vector2)
        cosine_similarity_list.append(cosine)

    return cosine_similarity_list




def get_complimentary_colors(input_color, comp_colors):
    comp_color_list = None
    for key in comp_colors.keys():
        input_colors = input_color.lower()
        if key.lower() == input_colors:
            comp_color_list = comp_colors[key]
   
    return comp_color_list

def get_contrast_colors(input_color, cont_colors):
    cont_color_list = None
    for key in cont_colors.keys():
        input_colors = input_color.lower()
        if key.lower() == input_colors:
            cont_color_list = cont_colors[key]

    return cont_color_list

def get_monochromatic_colors(input_color, mono_colors):
    mono_color_list = None
    for key in mono_colors.keys():
        input_colors = input_color.lower()
        if key.lower() == input_colors:
            mono_color_list = mono_colors[key]

    return mono_color_list

def get_pattern(pattern_input,mat_desc):

    cosine_similarity_list_for_pattren = []
    for text in mat_desc:
        text1 = str(text)
        text1 = text1.lower()
        text2 = str(pattern_input)
        text2 = text2.lower()

        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        cosine = get_cosine(vector1, vector2)
        cosine_similarity_list_for_pattren.append(cosine)
        

def perfrom_recommendations(df,input_dict):

    comp_colors = {
        'Red': ['green'],
        'Yellow': ['violet'],
        'Blue': ['orange'],
        'Green': ['red', 'yellow', 'blue'],
        'Orange': ['red', 'yellow', 'blue'],
        'Violet': ['yellow,' 'orange', 'green'],
        'Pink': ['yellow', 'green'],
        'White': ['black', 'red', 'blue'],
        'Black': ['white', 'red'],
        'Gray': ['red', 'white', 'black'],
        'Metallic gold': ['red', 'green', 'blue', 'yellow', 'violet'],
        'Metallic silver': ['blue', 'green', 'violet', 'pink']
    }
    cont_colors = {
        'Red': ['white', 'green', 'gold'],
        'Yellow': ['red', 'blue', 'green', 'pink'],
        'Blue': ['orange', 'pink', 'white', 'silver'],
        'Green': ['red', 'silver', 'gold', 'white'],
        'Orange': ['blue', 'yellow', 'purple', 'pink'],
        'Violet': ['white', 'pink', 'red', 'yellow'],
        'Pink': ['red', 'white', 'blue', 'gray', 'yellow'],
        'White': ['red', 'gray', 'black', 'pink', 'blue', 'green', 'yellow', 'red', 'silver'],
        'Black': ['white', 'gold', 'red', 'yellow'],
        'Gray': ['silver', 'white', 'black', 'pink', 'yellow', 'blue'],
        'Metallic gold': ['red', 'green', 'blue', 'yellow', 'violet'],
        'Metallic silver': ['blue', 'green', 'violet', 'pink']
    }
    mono_colors = {
        'Red': ['red'],
        'Yellow': ['yellow'],
        'Blue': ['blue'],
        'Green': ['green'],
        'Orange': ['orange'],
        'Violet': ['violet'],
        'Pink': ['pink'],
        'White': ['white'],
        'Black': ['black'],
        'Gray': ['gray'],
        'Metallic gold': ['old gold', 'gold yellow'],
        'Metallic silver': ['white', 'metallic silver']
    }

    mat_dic = {
        'silk': ['silk', 'satin', 'Linen-silk', 'blend', 'cotton-silk', 'blend'],
        'cotton': ['Cotton', 'silk'],
        'linen': ['linen', 'silk'],
        'satin': ['silk', 'satin'],
        'georgette': ['silk', 'satin'],
        'crepe': ['silk', 'satin'],
        'cotton silk blend': ['cotton', 'silk', 'blend', 'silk'],
        'linen silk blend': ['linen', 'silk', 'satin']
    }

    input_color = input_dict['Base_color']

    comp_recom_colors = get_complimentary_colors(input_color, comp_colors)
    cont_recom_colors = get_contrast_colors(input_color, cont_colors)
    mono_recom_colors = get_monochromatic_colors(input_color, mono_colors)
    

    comp_recom_colors = " ".join(comp_recom_colors)
    cont_recom_colors = " ".join(cont_recom_colors)
    mono_recom_colors = " ".join(mono_recom_colors)

    desc_text = df['Material Description'].to_list()

    # bug here.... Lets see (Solved )
    comp_similarity_list = get_cosine_similarity_list(desc_text, comp_recom_colors)
    cont_similarity_list = get_cosine_similarity_list(desc_text, cont_recom_colors)
    mono_similarity_list = get_cosine_similarity_list(desc_text, mono_recom_colors)
    # cont_similarity_list = []
    # mono_similarity_list = []


    comp_text_cosine_dic = get_text_cosine_dic(comp_similarity_list, desc_text)
    cont_text_cosine_dic = get_text_cosine_dic(cont_similarity_list, desc_text)
    mono_text_cosine_dic = get_text_cosine_dic(mono_similarity_list, desc_text)
    
    comp_sort_keys = sorted(comp_text_cosine_dic.keys(), reverse=True)
    cont_sort_keys = sorted(cont_text_cosine_dic.keys(), reverse=True)
    mono_sort_keys = sorted(mono_text_cosine_dic.keys(), reverse=True)
    
    comp_ind = recom_ind(comp_sort_keys, comp_text_cosine_dic)
    cont_ind = recom_ind(cont_sort_keys, cont_text_cosine_dic)
    mono_ind = recom_ind(mono_sort_keys, mono_text_cosine_dic)
    
    # paramters' colors for base color with all 3 categories (complimentary,contrast,monoschromatic)
    res_dic = {
        'complimentary':[comp_text_cosine_dic, comp_ind],
        'contrast':[cont_text_cosine_dic, cont_ind],
        'monochromatic':[mono_text_cosine_dic, mono_ind]
    }

    comp_df = df.iloc[comp_ind]
    cont_df = df.iloc[cont_ind]
    mono_df = df.iloc[mono_ind]


    if("acsent_color" in input_dict):
        # have to recommend pattern of any type
        
        comp_color  = match_color(input_dict['acsent_color'],comp_df['Material Description'])
        cont_color  = match_color(input_dict['acsent_color'],cont_df['Material Description'])
        mono_color  = match_color(input_dict['acsent_color'],mono_df['Material Description'])

        comp_df = comp_df.iloc[comp_color]
        cont_df = cont_df.iloc[cont_color]
        mono_df = mono_df.iloc[mono_color]

        comp_df =  comp_df[~comp_df["Material Description"].str.contains("Plain")]
        cont_df =  cont_df[~cont_df["Material Description"].str.contains("Plain")]
        mono_df =  mono_df[~mono_df["Material Description"].str.contains("Plain")]


        # return comp_df , cont_df , mono_df
    else:

        # have to return solid

        comp_color  = match_color(input_dict['pattern_color'],comp_df['Material Description'])
        cont_color  = match_color(input_dict['pattern_color'],cont_df['Material Description'])
        mono_color  = match_color(input_dict['pattern_color'],mono_df['Material Description'])

        comp_df = comp_df.iloc[comp_color]
        cont_df = cont_df.iloc[cont_color]
        mono_df = mono_df.iloc[mono_color]

        pat_comp = get_pattern_recommendation('Plain',comp_df['Material Description'])
        pat_cont = get_pattern_recommendation('Plain',cont_df['Material Description'])
        pat_mono = get_pattern_recommendation('Plain',mono_df['Material Description'])

        comp_df = comp_df.iloc[pat_comp]
        cont_df = cont_df.iloc[pat_cont]
        mono_df = mono_df.iloc[pat_mono]


        # return comp_df , cont_df , mono_df
    comp_mat = get_materials_recommendation(input_dict['material'],mat_dic,comp_df['Material Description'])
    comp_df = comp_df.iloc[comp_mat]

    cont_mat = get_materials_recommendation(input_dict['material'],mat_dic,cont_df['Material Description'])
    cont_df = cont_df.iloc[cont_mat]

    mono_mat = get_materials_recommendation(input_dict['material'],mat_dic,mono_df['Material Description'])
    mono_df = mono_df.iloc[mono_mat]

    return comp_df , cont_df , mono_df
        


