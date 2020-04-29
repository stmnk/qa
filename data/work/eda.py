import tensorflow.compat.v1 as tf
import gzip
import json
import collections
import os
import re

PATH = '../full/v1.0/train/nq-train-??.jsonl.gz'
# PATH = '../full/v1.0/train/nq-train-0?.jsonl.gz'
# PATH = '../full/v1.0/train/nq-train-00.jsonl.gz'
# PATH = './work-nq-train-00-03.jsonl.gz'
# PATH = './work-nq-train-00-99.jsonl.gz'
# TODO: use FLAGS for PATH params

BOOL_MARKERS = ['is', 'does', 'can', 'do', 'are', 'did', 'has', 'was']

def process_answer_candidates(line_dict):
    """
    :param line_dict:
    :return:
    """
    # TODO: split in distinct functionality

    annotations = line_dict['annotations']
    first_annotation = annotations[0]
    long_answer_start_token = first_annotation['long_answer']['start_token']
    long_answer_end_token = first_annotation['long_answer']['end_token']
    long_answer_start_byte = first_annotation['long_answer']['start_byte']
    long_answer_end_byte = first_annotation['long_answer']['end_byte']
    long_answer_candidate_index = first_annotation['long_answer']['candidate_index']

    question_text = line_dict['question_text']
    document_tokens = line_dict['document_tokens']

    # start_token = document_tokens[long_answer_start_token]
    # end_token = document_tokens[long_answer_end_token]
    # TODO: classify answers by token type

    long_answer_tokens_indices = document_tokens[int(long_answer_start_token):int(long_answer_end_token)]
    long_answer_html = ' '.join([x['token'] for x in long_answer_tokens_indices])

    short_answer_html = '-1'
    if len(first_annotation['short_answers']) > 0:
        short_answer_start_token = first_annotation['short_answers'][0]['start_token']
        short_answer_end_token = first_annotation['short_answers'][0]['end_token']
        short_answer_tokens = document_tokens[int(short_answer_start_token):int(short_answer_end_token)]
        short_answer_html = ' '.join([x['token'] for x in short_answer_tokens])

    boolean_answer = first_annotation['yes_no_answer']

    new_line = collections.OrderedDict({
        'question_text': question_text,
        'boolean_answer': boolean_answer,
        'long_answer_html': long_answer_html,
        'short_answer_html': short_answer_html,
        'long_answer_start_index': long_answer_start_token,
        'long_answer_end_index': long_answer_start_token,
        'long_answer_start_byte': long_answer_start_byte,
        'long_answer_end_byte': long_answer_end_byte,
        'long_answer_candidate_index': long_answer_candidate_index
    })

    new_line.update(line_dict)

    return new_line


def get_data(path_pattern):
    for input_path in tf.gfile.Glob(path_pattern):
        print(input_path)
        with gzip.GzipFile(fileobj=tf.gfile.Open(input_path, "rb")) as input_file:
            for line in input_file:
                line_dict = json.loads(line, object_pairs_hook=collections.OrderedDict)
                del line_dict['document_url']
                del line_dict['document_title']

                processed_line = process_answer_candidates(line_dict)
                yield processed_line


def write_jsonl(data, output_path, append=False, log=True):
    """
    Write list of objects to a JSON lines file.
    """
    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + '\n')
    if log:
        print(f'Wrote {len(data)} records to {output_path}')


def drop_column(json_object, column_name_string):
    del json_object[column_name_string]
    return json_object


def drop_columns(json_object, column_names_list):
    new_json_object = json_object
    for name in column_names_list:
        new_json_object = drop_column(new_json_object, name)
    return new_json_object


def filter_boolean(line):
    return line['boolean_answer'] != 'NONE'


def q_bool_marker(line):
    bmk = ['is ', 'does ', 'can ', 'do ', 'are ', 'did ', 'has ', 'was ']
    rx = re.compile('^(' + '|'.join(bmk) + ')')
    tgmk = ['<Ol> ', '<Ul> ', '<Li> ', '<Table> ', '<Tr> '] # TODO: add '<P> ',
    rxtg = re.compile('^(' + '|'.join(tgmk) + ')')
    return (
        line['boolean_answer'] == 'NONE'
        and line['short_answer_html'] == '-1'
        and rxtg.match(line['long_answer_html']) is not None
        and rx.match(line['question_text']) is not None
    )

# TODO: builder pattern for applying filters in chain
def filter_data(output_file_pattern, input_files_path, filter_criteria, columns_to_drop, overwrite_flag=False):
    if overwrite_flag:
        os.remove(output_file_pattern)
    for line in get_data(input_files_path):
        if 'boolean_answer_defined' in filter_criteria:
            if filter_boolean(line):
                drop_columns(line, columns_to_drop)
                write_jsonl([line], output_file_pattern, append=True, log=False)  # TODO: isolate I/O
        if 'boolean_answer_missing_and_q_bool_marker' in filter_criteria:
            if q_bool_marker(line):
                # print('boom!')
                drop_columns(line, columns_to_drop)
                write_jsonl([line], output_file_pattern, append=True, log=True)  # TODO: isolate I/O


def main(_):
    # output_file_pattern = 'my_data.jsonl'
    output_file_pattern = 'data_boolean_la_only.jsonl'
    # filter_criteria = ['boolean_answer_defined']
    filter_criteria = ['boolean_answer_missing_and_q_bool_marker']
    columns_to_drop = [
        'annotations',
        'question_tokens',
        'document_tokens', 'document_html',
        'short_answer_html',
        'long_answer_start_index', 'long_answer_end_index',
        'long_answer_start_byte', 'long_answer_end_byte',
        'long_answer_candidate_index', 'long_answer_candidates',
    ]
    filter_data(output_file_pattern, PATH, filter_criteria, columns_to_drop, overwrite_flag=False)


if __name__ == "__main__":
    tf.app.run()

# gzip -c work-nq-train-00-03.jsonl > work-nq-train-00-03.jsonl.gz
# ~6K questions per file x 50 files = 300 K questions
# boolean answers: Wrote 3798 records to my_data.jsonl
# 4094 - 3798 = 296 (is/does)
# 4277 - 4094 = 183 (can/do/are/did/has/was)
# - 4277 = (lists & tables)

# nq-train-00 remove all              -> 20 MB      nq-train-?? -> 1 GB
# nq-train-00 remove annotations only -> 80 MB      nq-train-?? -> 4 GB

