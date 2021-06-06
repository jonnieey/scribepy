# Copyright(c) 2006 Eric Faurot <eric.faurot@gmail.com>
# See LICENSE for details.

# Python 3 adaptation by Maxim Kolosov

# CHAR_CODEC = 'utf-8'
CHAR_CODEC = "cp1251"

from sys import hexversion

if hexversion < 0x03000000:
    _range = xrange
    _chr = chr
else:
    _range = range

    def _chr(value):
        return bytes([value])


import struct

_crc = (
    0x00000000,
    0x04C11DB7,
    0x09823B6E,
    0x0D4326D9,
    0x130476DC,
    0x17C56B6B,
    0x1A864DB2,
    0x1E475005,
    0x2608EDB8,
    0x22C9F00F,
    0x2F8AD6D6,
    0x2B4BCB61,
    0x350C9B64,
    0x31CD86D3,
    0x3C8EA00A,
    0x384FBDBD,
    0x4C11DB70,
    0x48D0C6C7,
    0x4593E01E,
    0x4152FDA9,
    0x5F15ADAC,
    0x5BD4B01B,
    0x569796C2,
    0x52568B75,
    0x6A1936C8,
    0x6ED82B7F,
    0x639B0DA6,
    0x675A1011,
    0x791D4014,
    0x7DDC5DA3,
    0x709F7B7A,
    0x745E66CD,
    0x9823B6E0,
    0x9CE2AB57,
    0x91A18D8E,
    0x95609039,
    0x8B27C03C,
    0x8FE6DD8B,
    0x82A5FB52,
    0x8664E6E5,
    0xBE2B5B58,
    0xBAEA46EF,
    0xB7A96036,
    0xB3687D81,
    0xAD2F2D84,
    0xA9EE3033,
    0xA4AD16EA,
    0xA06C0B5D,
    0xD4326D90,
    0xD0F37027,
    0xDDB056FE,
    0xD9714B49,
    0xC7361B4C,
    0xC3F706FB,
    0xCEB42022,
    0xCA753D95,
    0xF23A8028,
    0xF6FB9D9F,
    0xFBB8BB46,
    0xFF79A6F1,
    0xE13EF6F4,
    0xE5FFEB43,
    0xE8BCCD9A,
    0xEC7DD02D,
    0x34867077,
    0x30476DC0,
    0x3D044B19,
    0x39C556AE,
    0x278206AB,
    0x23431B1C,
    0x2E003DC5,
    0x2AC12072,
    0x128E9DCF,
    0x164F8078,
    0x1B0CA6A1,
    0x1FCDBB16,
    0x018AEB13,
    0x054BF6A4,
    0x0808D07D,
    0x0CC9CDCA,
    0x7897AB07,
    0x7C56B6B0,
    0x71159069,
    0x75D48DDE,
    0x6B93DDDB,
    0x6F52C06C,
    0x6211E6B5,
    0x66D0FB02,
    0x5E9F46BF,
    0x5A5E5B08,
    0x571D7DD1,
    0x53DC6066,
    0x4D9B3063,
    0x495A2DD4,
    0x44190B0D,
    0x40D816BA,
    0xACA5C697,
    0xA864DB20,
    0xA527FDF9,
    0xA1E6E04E,
    0xBFA1B04B,
    0xBB60ADFC,
    0xB6238B25,
    0xB2E29692,
    0x8AAD2B2F,
    0x8E6C3698,
    0x832F1041,
    0x87EE0DF6,
    0x99A95DF3,
    0x9D684044,
    0x902B669D,
    0x94EA7B2A,
    0xE0B41DE7,
    0xE4750050,
    0xE9362689,
    0xEDF73B3E,
    0xF3B06B3B,
    0xF771768C,
    0xFA325055,
    0xFEF34DE2,
    0xC6BCF05F,
    0xC27DEDE8,
    0xCF3ECB31,
    0xCBFFD686,
    0xD5B88683,
    0xD1799B34,
    0xDC3ABDED,
    0xD8FBA05A,
    0x690CE0EE,
    0x6DCDFD59,
    0x608EDB80,
    0x644FC637,
    0x7A089632,
    0x7EC98B85,
    0x738AAD5C,
    0x774BB0EB,
    0x4F040D56,
    0x4BC510E1,
    0x46863638,
    0x42472B8F,
    0x5C007B8A,
    0x58C1663D,
    0x558240E4,
    0x51435D53,
    0x251D3B9E,
    0x21DC2629,
    0x2C9F00F0,
    0x285E1D47,
    0x36194D42,
    0x32D850F5,
    0x3F9B762C,
    0x3B5A6B9B,
    0x0315D626,
    0x07D4CB91,
    0x0A97ED48,
    0x0E56F0FF,
    0x1011A0FA,
    0x14D0BD4D,
    0x19939B94,
    0x1D528623,
    0xF12F560E,
    0xF5EE4BB9,
    0xF8AD6D60,
    0xFC6C70D7,
    0xE22B20D2,
    0xE6EA3D65,
    0xEBA91BBC,
    0xEF68060B,
    0xD727BBB6,
    0xD3E6A601,
    0xDEA580D8,
    0xDA649D6F,
    0xC423CD6A,
    0xC0E2D0DD,
    0xCDA1F604,
    0xC960EBB3,
    0xBD3E8D7E,
    0xB9FF90C9,
    0xB4BCB610,
    0xB07DABA7,
    0xAE3AFBA2,
    0xAAFBE615,
    0xA7B8C0CC,
    0xA379DD7B,
    0x9B3660C6,
    0x9FF77D71,
    0x92B45BA8,
    0x9675461F,
    0x8832161A,
    0x8CF30BAD,
    0x81B02D74,
    0x857130C3,
    0x5D8A9099,
    0x594B8D2E,
    0x5408ABF7,
    0x50C9B640,
    0x4E8EE645,
    0x4A4FFBF2,
    0x470CDD2B,
    0x43CDC09C,
    0x7B827D21,
    0x7F436096,
    0x7200464F,
    0x76C15BF8,
    0x68860BFD,
    0x6C47164A,
    0x61043093,
    0x65C52D24,
    0x119B4BE9,
    0x155A565E,
    0x18197087,
    0x1CD86D30,
    0x029F3D35,
    0x065E2082,
    0x0B1D065B,
    0x0FDC1BEC,
    0x3793A651,
    0x3352BBE6,
    0x3E119D3F,
    0x3AD08088,
    0x2497D08D,
    0x2056CD3A,
    0x2D15EBE3,
    0x29D4F654,
    0xC5A92679,
    0xC1683BCE,
    0xCC2B1D17,
    0xC8EA00A0,
    0xD6AD50A5,
    0xD26C4D12,
    0xDF2F6BCB,
    0xDBEE767C,
    0xE3A1CBC1,
    0xE760D676,
    0xEA23F0AF,
    0xEEE2ED18,
    0xF0A5BD1D,
    0xF464A0AA,
    0xF9278673,
    0xFDE69BC4,
    0x89B8FD09,
    0x8D79E0BE,
    0x803AC667,
    0x84FBDBD0,
    0x9ABC8BD5,
    0x9E7D9662,
    0x933EB0BB,
    0x97FFAD0C,
    0xAFB010B1,
    0xAB710D06,
    0xA6322BDF,
    0xA2F33668,
    0xBCB4666D,
    0xB8757BDA,
    0xB5365D03,
    0xB1F740B4,
)


def checksum(header, body):
    reg = 0
    for c in header:
        reg = ((reg << 8) & 0xFFFFFFFF) ^ _crc[((reg >> 24) & 0xFF) ^ ord(c)]
    for i in (0, 0, 0, 0):
        reg = ((reg << 8) & 0xFFFFFFFF) ^ _crc[((reg >> 24) & 0xFF) ^ i]
    for c in body:
        reg = ((reg << 8) & 0xFFFFFFFF) ^ _crc[((reg >> 24) & 0xFF) ^ ord(c)]
    return reg


def split_segments(data, segs):
    segments = []
    start = 0
    stop = 0
    map_segs = segs
    if hexversion < 0x03000000:
        map_segs = map(ord, segs)
    for length in map_segs:
        if length:
            stop += length
            segments.append(data[start:stop])
            start = stop
        else:
            segments.append(b"")
    return segments


def segmentsToPackets(segments):
    packets = []
    packet = []
    for segment in segments:
        packet.append(segment)
        if len(segment) != 255:
            packets.append(b"".join(packet))
            packet = []
    return packets, packet


class OggPage(object):
    version = 0
    headerType = None
    streamID = None
    granulePosition = None
    sequenceNumber = None
    segments = None
    checksum = None
    rawData = None

    def continued(self):
        return self.segments[-1] == 255

    continued = property(continued)

    def packetCount(self):
        return len([s for s in self.segments if len(s) != 255])

    def getPackets(self):
        return segmentsToPackets(self.segments)

    def dataLength(self):
        return sum(map(len, self.segments))

    def pageOverhead(self):
        return 27 + len(self.segments)

    def payload(self):
        return self.pageOverhead() + self.dataLength()

    def pack(self):
        header = struct.pack(
            "<4sBBqLL",
            b"OggS",
            self.version,
            self.headerType,
            self.granulePosition,
            self.streamID,
            self.sequenceNumber,
        )

        def _(s):
            return _chr(len(s))

        body = b"".join(
            [_chr(len(self.segments))] + map(_, self.segments) + self.segments
        )
        return b"".join(
            [header, struct.pack("<L", checksum(header, body)), body]
        )

    def __repr__(self):
        return "<OggPage version=%r headerType=%r streamID=%r granulePosition=%r sequenceNumber=%r continued=%r segments=%r payload=%r>" % (
            self.version,
            self.headerType,
            self.streamID,
            self.granulePosition,
            self.sequenceNumber,
            self.continued,
            len(self.segments),
            self.payload(),
        )


class iobuffer(object):
    def __init__(self, data=b""):
        self.data = data
        self.offset = 0
        self.bytes = 0
        self.length = len(data)

    def write(self, data):
        self.data = b"".join([self.data[self.offset :], data])
        self.offset = 0
        self.length += len(data)

    def __len__(self):
        return self.length

    def read(self, count):
        assert self.length >= count
        chunk = self.data[self.offset : self.offset + count]
        self.length -= count
        self.offset += count
        self.bytes += len(chunk)
        return chunk

    def unpack(self, format, size=None):
        if size is None:
            size = struct.calcsize(format)
        return struct.unpack(format, self.read(size))

    def unread(self, data):
        self.data = b"".join([data, self.data[self.offset :]])
        self.offset = 0
        self.length += len(data)


class Parser(object):
    expected = 0
    processed = 0

    def __init__(self, expected):
        self._buffer = iobuffer()
        self.expected = expected

    def buffered(self):
        return self._buffer.data[self._buffer.offset :]

    def required(self):
        return self.expected - len(self._buffer)

    def process(self, data):
        self._buffer.write(data)
        while len(self._buffer) >= self.expected:
            chunk = self._buffer.read(self.expected)
            try:
                self.expected = self.processChunk(chunk)
                self.processed += len(chunk)
            except:
                raise

    def processChunk(self, chunk):
        raise NotImplementedError


class OggReader(Parser):
    pages = 0
    HEADER_LENGTH = 27

    def __init__(self):
        Parser.__init__(self, self.HEADER_LENGTH)
        self.__currentPage = None
        self.processChunk = self.processHeader

    def processHeader(self, data):
        self.__currentPage = p = OggPage()
        (
            magic,
            p.version,
            p.headerType,
            p.granulePosition,
            p.streamID,
            p.sequenceNumber,
            p.checksum,
            nseg,
        ) = struct.unpack("<4sBBqLLLB", data)
        if magic != b"OggS":
            raise ValueError("Not an ogg page")
        self.__raw = [data]
        self.processChunk = self.processSegmentTable
        return nseg

    def processSegmentTable(self, data):
        self.__segmentTable = data
        self.__raw.append(data)
        self.processChunk = self.processSegments
        if hexversion < 0x03000000:
            return sum(map(ord, data))
        else:
            return sum(data)

    def processSegments(self, data):
        page = self.__currentPage
        page.segments = split_segments(data, self.__segmentTable)
        self.__raw.append(data)
        page.rawData = b"".join(self.__raw)
        self.pageReceived(page)
        self.pages += 1
        self.processChunk = self.processHeader
        return self.HEADER_LENGTH

    def outOfBandDataReceived(self, data):
        pass

    def pageReceived(self, page):
        raise NotImplementedError


class OggDemultiplexer(OggReader):
    def __init__(self):
        OggReader.__init__(self)
        self.streams = {}
        self.readingHeaders = True

    def buildStream(self, packet):
        return self.streamFactory(self, packet)

    def pageReceived(self, page):
        if self.readingHeaders:
            if page.headerType & 0x02:
                assert page.headerType & 0x01 == 0
                assert page.headerType & 0x04 == 0
                assert page.streamID not in self.streams
                assert not page.continued
                packets, left = page.getPackets()
                assert len(packets) == 1
                stream = self.buildStream(packets[0])
                stream.processPage(page)
                self.streams[page.streamID] = stream
                return
            self.readingHeaders = False
        assert page.headerType & 0x02 == 0
        assert page.streamID in self.streams
        stream = self.streams[page.streamID]
        stream.processPage(page)
        if page.headerType & 0x04:
            stream.endStream()
            del self.streams[page.streamID]
            if len(self.streams) == 0:
                self.allStreamsEnded()

    def outOfBandPageReceived(self, page):
        pass

    def allStreamsEnded(self):
        self.readingHeaders = True


class SimpleDemultiplexer(OggDemultiplexer):
    def __init__(self, streamReader):
        OggDemultiplexer.__init__(self)
        self.streamReader = streamReader

    def buildStream(self, packet):
        assert len(self.streams) == 0
        return self.streamReader


class VorbisIdentification(object):
    version = None
    audioChannels = None
    sampleRate = None
    maximumBitrate = None
    nominalBitrate = None
    minimumBitrate = None
    blocksize = None
    # ~ PACKET_HEADER = chr(1) + b'vorbis'
    PACKET_HEADER = b"\x01vorbis"

    def __repr__(self):
        return "<VorbisIdentification version=%r audioChannels=%r sampleRate=%r bitrates=[ %r, %r, %r ] blocksize=%r>" % (
            self.version,
            self.audioChannels,
            self.sampleRate,
            self.minimumBitrate,
            self.nominalBitrate,
            self.maximumBitrate,
            self.blocksize,
        )

    def positionToSeconds(self, position):
        return float(position) / self.sampleRate

    def pack(self):
        return "".join(
            [
                self.PACKET_HEADER,
                s.pack(
                    "<IBIiiiBB",
                    self.version,
                    self.audioChannels,
                    self.sampleRate,
                    self.maximumBitrate,
                    self.nominalBitrate,
                    self.minimumBitrate,
                    self.blocksize,
                    1,
                ),
            ]
        )


class VorbisComments(object):
    vendor = None
    comments = None
    # ~ PACKET_HEADER = chr(3) + b'vorbis'
    PACKET_HEADER = b"\x03vorbis"

    def pack(self):
        vendor = self.vendor.encode(CHAR_CODEC)
        data = [
            self.PACKET_HEADER,
            struct.pack("<L", len(vendor)),
            vendor,
            struct.pack("<L", len(self.comments)),
        ]
        for key, value in self.comments:
            key = key.upper()
            value = value.encode(CHAR_CODEC)
            data.append(struct.pack("<L", len(key) + 1 + len(value)))
            data.append(key)
            data.append(b"=")
            data.append(value)
        data.append(b"\x01")
        return "".join(data)


class VorbisSetup(object):
    codebooks = None
    timeDomainTransforms = None
    floorType = None
    residues = None
    mappings = None
    modes = None
    # ~ PACKET_HEADER = chr(5) + b'vorbis'
    PACKET_HEADER = b"\x05vorbis"

    def pack(self):
        return self.rawPacket


class OggStreamReader(object):
    pages = 0
    __segments = None

    def endStream(self):
        pass

    def processPage(self, page):
        position = page.granulePosition
        if self.__segments is None:
            self.__segments = []
        self.__segments.extend(page.segments)
        packets, self.__segments = segmentsToPackets(self.__segments)
        if packets:
            self.packetsReceived(packets, position)
        else:
            assert position == -1
        self.pages += 1

    def packetsReceived(self, packets, position):
        pass


class VorbisStreamReader(OggStreamReader):
    identification = None
    comments = None
    setup = None

    def __init__(self):
        OggStreamReader.__init__(self)
        self.__expected = "identification"

    def packetsReceived(self, packets, position):
        if not self.__expected:
            return self.audioPacketsReceived(packets, position)
        assert position == 0
        for packet in packets:
            handler = getattr(self, "read_%s" % self.__expected)
            handler(packet)

    def read_identification(self, packet):
        s = iobuffer(packet)
        header = VorbisIdentification.PACKET_HEADER
        assert s.read(len(header)) == header
        i = VorbisIdentification()
        (
            i.version,
            i.audioChannels,
            i.sampleRate,
            i.maximumBitrate,
            i.nominalBitrate,
            i.minimumBitrate,
            i.blocksize,
            framingFlag,
        ) = s.unpack("<IBIiiiBB")
        assert len(s) == 0
        self.__expected = "comments"
        self.identificationReceived(i)

    def read_comments(self, packet):
        s = iobuffer(packet)
        header = VorbisComments.PACKET_HEADER
        assert s.read(len(header)) == header
        (length,) = s.unpack("<L")
        comments = VorbisComments()
        comments.vendor = s.read(length).decode(CHAR_CODEC)
        comments.comments = []
        (ncomments,) = s.unpack("<L")
        for i in _range(ncomments):
            (length,) = s.unpack("<L")
            key, value = s.read(length).split(b"=", 1)
            comments.comments.append([key.upper(), value.decode(CHAR_CODEC)])
        assert s.read(1) == b"\x01"
        assert len(s) == 0
        self.__expected = "setup"
        self.commentsReceived(comments)

    def read_setup(self, packet):
        assert packet.startswith(VorbisSetup.PACKET_HEADER)
        setup = VorbisSetup()
        setup.rawPacket = packet
        self.__expected = None
        self.setupReceived(setup)

    def identificationReceived(self, identification):
        self.identification = identification

    def commentsReceived(self, comments):
        self.comments = comments

    def setupReceived(self, setup):
        self.setup = setup

    def audioPacketsReceived(self, packets, position):
        pass


class VorbisStreamInfo(VorbisStreamReader):
    lastPosition = None
    startPosition = None
    payload = 0
    overhead = 0
    pageCount = 0
    audioPackets = 0
    audioPacketLength = 0
    stop = 0
    start = 0

    def pageReceived(self, page):
        self.pageCount += 1
        self.payload += page.payload()
        self.overhead += page.pageOverhead()
        VorbisStreamReader.pageReceived(self, page)

    def audioPacketsReceived(self, packets, position):
        if self.startPosition is None:
            self.startPosition = position
        self.lastPosition = position
        self.audioPackets += len(packets)
        self.audioPacketLength += sum(map(len, packets))

    def identificationReceived(self, identification):
        self.identification = identification

    def setupReceived(self, setup):
        self.setup = setup

    def commentsReceived(self, comments):
        self.comments = comments

    def endStream(self):
        self.stop = self.identification.positionToSeconds(self.lastPosition)
        self.start = self.identification.positionToSeconds(self.startPosition)


if __name__ == "__main__":
    from sys import hexversion

    info = VorbisStreamInfo()
    stream = SimpleDemultiplexer(info)
    stream.process(open("test.ogg", "rb").read())
    print("size            : %d" % info.payload)
    print("overhead        : %d" % info.overhead)
    print("pages           : %d" % info.pageCount)
    print("audio packets   : %d" % info.audioPackets)
    print("audio length    : %d" % info.audioPacketLength)
    print("vendor          : %s" % info.comments.vendor)
    print("comment entries : %d" % len(info.comments.comments))
    for key, value in info.comments.comments:
        if hexversion < 0x03000000:
            print("- %s: %s" % (key, value.encode(CHAR_CODEC)))
        else:
            print("- %s: %s" % (key, value))
    print("sample rate     : %d" % info.identification.sampleRate)
    print("audio channels  : %d" % info.identification.audioChannels)
    print("nominal bitrate : %d" % info.identification.nominalBitrate)
    print("first frame     : %fs" % info.start)
    import datetime

    print(
        "duration        : %s"
        % datetime.timedelta(seconds=info.stop - info.start)
    )
