#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" symbol_scanner
  Copyright 2020 Slash Gordon
  Use of this source code is governed by an MIT-style license that
  can be found in the LICENSE file.
"""
import logging
import os
import pickle
import sys

import argparse
import pandas as pd
import wikipedia as wp
import wptools
from pytickersymbols import PyTickerSymbols, Statics
from difflib import SequenceMatcher
import multiprocessing
from symbol_scanner.index_definitions import Indices
from symbol_scanner.scanner import SymbolScanner
from symbol_scanner.word_score import get_word_list_diff

logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='SymbolScanner CLI'
    )
    parser.add_argument('--cache', action="store_true", default=False)
    args = parser.parse_args()
    scanner = SymbolScanner(args.cache)
    stock_data = PyTickerSymbols()
    indices = stock_data.get_all_indices()
    # missing stocks in index
    for index in indices:
        stocks = stock_data.get_stocks_by_index(index)
        py_stocks = list(map(lambda x: x['name'], stocks))
        wiki_stocks = [
            wiki_stock for wiki_stock in scanner.data[index]['name']
        ]
        missing_stocks = get_word_list_diff(wiki_stocks, py_stocks)
        scanner.log.info(f'-------missing stocks of {index}---------')
        for stock in missing_stocks:
            scanner.log.info(stock)
        scanner.log.info(f'-------wrong stocks of {index}---------')
        old_stocks = get_word_list_diff(py_stocks, wiki_stocks)
        for stock in old_stocks:
            scanner.log.info(stock)