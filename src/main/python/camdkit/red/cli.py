#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) Society of Motion Picture and Television Engineers
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''RED CLI tool'''

import json
import argparse
import camdkit.red.reader

def main():
  parser = argparse.ArgumentParser(description="Conver RED camera metadata to JSON according to the OSVP Camera Metadata Model.")
  parser.add_argument(
    'meta_3_file_path',
    type=str,
    help="Path to CSV file generated using REDline (`REDline --silent --i <camera_file_path> --printMeta 3`)"
    )
  parser.add_argument(
    'meta_5_file_path',
    type=str,
    help="Path to CSV file generated using REDline (`REDline --silent --i <camera_file_path> --printMeta 5`)"
    )

  args = parser.parse_args()

  with open(args.meta_3_file_path, "r", encoding="utf-8") as type_3_file, \
    open(args.meta_5_file_path, "r", encoding="utf-8") as type_5_file:
    clip = camdkit.red.reader.to_clip(type_3_file, type_5_file)

  print(json.dumps(clip.to_json(), indent=2))

if __name__ == "__main__":
  main()
