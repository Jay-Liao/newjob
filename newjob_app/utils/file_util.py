#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json


def save_dict_as_json_file(file_path, dict_data):
    with open(file_path, "w") as outfile:
        json.dump(dict_data, outfile)


def read_dict_from_json_file(file_path):
    with open(file_path, "r") as input_file:
        data = json.load(input_file)
        return data


def make_dirs(path):
    try:
        os.makedirs(path)
    except:
        pass
