# this is an EFI binary from a silion vendor that has embedded coSWID in the .SBAT section
#
# $ objdump -s -j .sbom fwupdx64.efi
#
# fwupdx64.efi:     file format pei-x86-64
#
# Contents of section .sbom:
#  14000 bf0f6565 6e2d5553 0050b84e d8eda7b1  ..een-US.P.N....
#  14010 502f83f6 90132e68 adef08f5 01686677  P/.....h.....hfw
#  14020 75706478 36340d63 312e350e 19400005  updx64.c1.5..@..
#  14030 bf183265 66777570 64183778 26454649  ..2efwupd.7x&EFI
#  14040 2068656c 70657273 20746f20 696e7374   helpers to inst
#  14050 616c6c20 73797374 656d2066 69726d77  all system firmw
#  14060 61726518 2d6f312e 342d3139 2d673264  are.-o1.4-19-g2d
#  14070 38636231 64ff029f bf181f6e 52696368  8cb1d......nRich
#  14080 61726420 48756768 65731820 6b687567  ard Hughes. khug
#  14090 68736965 2e636f6d 18219f06 01ffffff  hsie.com.!......
#  140a0 049fbf18 26782768 74747073 3a2f2f73  ....&x'https://s
#  140b0 7064782e 6f72672f 6c696365 6e736573  pdx.org/licenses
#  140c0 2f4c4750 4c2d322e 302e6874 6d6c1828  /LGPL-2.0.html.(
#  140d0 21ffffff                             !...

sbom_static += files('fwupdx64.efi')

# this is a firmware file from the vendor -- we don't know what it is -- and we can't load it
# as a PE or ELF elf -- but it does have an embedded uSWID section we can locate and consume
#
# $ xxd ec-firmware.bin
# 00000000: dead beef dead beef dead beef dead beef  ................
# 00000010: dead beef dead beef 5342 4f4d d6ba 2eac  ........SBOM....
# 00000020: a3e6 7a52 aaee 3baf 0117 0098 0000 00a9  ..zR..;.........
# 00000030: 0f65 656e 2d55 5300 5021 242f f8e2 c658  .een-US.P!$/...X
# 00000040: 01a4 f380 7acc 08a2 d208 f501 6d4d 6f64  ....z.......mMod
# 00000050: 656d 4261 7365 6261 6e64 0d68 3131 2e32  emBaseband.h11.2
# 00000060: 322e 3333 0e01 05a2 1832 6575 5357 4944  2.33.....2euSWID
# 00000070: 182d 7828 6232 6564 3666 3165 6438 3538  .-x(b2ed6f1ed858
# 00000080: 3762 6630 3161 3239 3531 6437 3435 3132  7bf01a2951d74512
# 00000090: 6137 3066 3161 3531 3264 3338 0281 a318  a70f1a512d38....
# 000000a0: 1f6f 4875 6768 736b 6920 4c69 6d69 7465  .oHughski Limite
# 000000b0: 6418 206b 6875 6768 736b 692e 636f 6d18  d. khughski.com.
# 000000c0: 2183 0104 0204 80de adbe efde adbe efde  !...............
# 000000d0: adbe efde adbe efde adbe efde adbe efde  ................
sbom_static += files('ec-firmware.bin')
