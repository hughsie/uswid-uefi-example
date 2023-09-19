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
