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

'''Canon camera reader'''

import csv
import typing
import struct
from fractions import Fraction

import camdkit.model

def _read_float32_as_hex(float32_hex: str) -> float:
  return struct.unpack('>f', bytes.fromhex(float32_hex))[0]

def to_clip(static_csv: typing.IO, frames_csv: typing.IO) -> camdkit.model.Clip:
  """Read Canon camera metadata into a `Clip`.
  `static_csv`: Static camera metadata.
  `frames_csv`: Per-frame camera metadata.
  """

  # read clip metadata
  clip_metadata = next(csv.DictReader(static_csv))
  clip = camdkit.model.Clip()

  # read frame metadata
  frame_data = list(csv.DictReader(frames_csv))
  first_frame_data = frame_data[0]

  # clip metadata

  # duration
  clip.duration = Fraction(int(clip_metadata["Duration"]), int(clip_metadata["Timescale"]))

  # anamorphic_squeeze
  lens_squeeze_factor = int(clip_metadata["LensSqueezeFactor"])
  if lens_squeeze_factor == 0:
    clip.anamorphic_squeeze = 100
  elif lens_squeeze_factor == 1:
    clip.anamorphic_squeeze = 133
  elif lens_squeeze_factor == 2:
    clip.anamorphic_squeeze = 200
  elif lens_squeeze_factor == 3:
    clip.anamorphic_squeeze = 180

  # ISO
  if int(first_frame_data['PhotographicSensitivityMode']) == 1:
    clip.iso = Fraction(first_frame_data['PhotographicSensitivity']).numerator - 0x80000000

  # clip.active_sensor_physical_dimensions is not supported
  # clip.capture_fps is no supported

  clip.camera_make = "Canon"

  # shutter angle
  clip.shutter_angle = round(Fraction(first_frame_data['ExposureTime']) * 1000)

  # sampled metadata

  # focal_length
  clip.focal_length = tuple(round(Fraction(m["FocalLength"])) for m in frame_data)

  # focal_position
  clip.focal_position = tuple(round(_read_float32_as_hex(m["FocusPosition"]) * 1000) for m in frame_data)

  # entrance_pupil_position not supported

  # t_number
  if int(first_frame_data['ApertureMode']) == 2:
    clip.t_number = tuple(round(Fraction(m["ApertureNumber"]) * 1000) for m in frame_data)
  elif int(first_frame_data['ApertureMode']) == 1:
    clip.f_number = tuple(round(Fraction(m["ApertureNumber"]) * 1000) for m in frame_data)

  return clip
