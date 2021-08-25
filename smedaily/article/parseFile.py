import re
from bs4 import BeautifulSoup
import json


def iter_docs(author):
    author_attr = author.attrib
    for doc in author.iter('document'):
        doc_dict = author_attr.copy()
        doc_dict.update(doc.attrib)
        doc_dict['data'] = doc.text
        yield doc_dict


def get_children_data(tree):
    if tree.name is None or tree.name == 'style':
        return None
    if tree.name == 'table-group' or tree.name == 'table':
        return {'table': '<<< 세부 내용 테이블 참조 >>>'}
    children = [child for child in tree.children]
    if len(children) == 1:
        if tree.name:
            if tree.string is not None:
                text = re.sub(' +', ' ', tree.string.replace('&cr', '').replace('\n', ''))
                return text
    else:
        result = {}
        for index, child in enumerate(children):
            child_data = get_children_data(child)
            if child_data:
                result[child.name + ' ' + str(index)] = child_data
        return result


def xml_to_dict(xml_file):
    result = {}
    tree = BeautifulSoup(xml_file, 'html.parser')
    body_data = get_children_data(tree.body)
    result['data'] = body_data
    return result


def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]


def get_summary(data):
    data_dict = xml_to_dict(data)
    data_json = json.dumps(data_dict, indent=2, ensure_ascii=False)
    return data_dict
