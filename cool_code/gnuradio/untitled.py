#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: basic
# GNU Radio version: 3.10.1.1

from gnuradio import audio
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class untitled(gr.top_block):

    def __init__(self, samp_rate=48000):
        gr.top_block.__init__(self, "basic", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/minamina/test.wav', False)
        self.audio_sink_0 = audio.sink(44100, '', True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_wavfile_source_0, 0), (self.audio_sink_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-r", "--samp-rate", dest="samp_rate", type=intx, default=48000,
        help="Set Sample rate [default=%(default)r]")
    return parser


def main(top_block_cls=untitled, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(samp_rate=options.samp_rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()