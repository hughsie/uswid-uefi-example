# uswid-uefi-example

First I think it makes sense to define what we want, and why we need it before working out what
we’ve already got, and what we need to add.

To me, the purpose of an SBoM is so that the user knows *what* components make up the software
deliverable, and gives them information on *who* built each part.
I don’t think it has to include the *how* or the *why*, as the questions we need to answer are
things like “what version of OpenSSL is included” and “do I trust all the companies contributing
code and binaries to this image”.
I think security triage, analysis and mechanisms like VEX are important, but step 1 has to be the
*what* and the *who* and step 2 can then use the *what* and *who* to add more metadata such as VEX.

The latter of *what* and *who* seems easier to define.
The *who*, in SWID nomenclature is the legal entity responsible for something.
This could be the upstream maintainer of the open source library, the silicon vendor providing a
binary FSP, or the IBV providing code to the ODM that is compiling it into a binary for the OEM.
Each entity can be just one role, or have multiple roles, and I don’t think at this point we need
to worry about the mapping too closely; the pragmatist in me says we shouldn’t make too many
additional business relationships public that are not already public to avoid needing lengthy
legal approval.

From a uSWID point of view, to define an entity we just need to know the legal name, the
registration ID (e.g. a URL, or reverse DNS entry like `com.intel`) and the roles that entity is taking.

The *what* is slightly harder to define. My middle ground here would be to suggest that any
component that can be removed, replaced or added to a UEFI file volume should be included, as should
library and compiler versions that make sense.
The latter would include libraries that a security researcher might be interested in (perhaps
because of previous security issues) or that companies might need to enumerate for compliance reasons.
The former would include DXEs, PEIMs, uCODE, FSP, EC, OptionROM – but not things like encryption keys
or source code references.

Each component we define should therefore have at least one entity that claims roles on it.
For instance, Intel FSP is created by Intel, maintained by Intel, and distributed by Intel.
A modified DXE might be originally created by Intel in EDK2, but be modified by and maintained by
AMI and distributed by Lenovo. Similarly, an image loader like libpng might be maintained by the
upstream community, be unmodified, and be distributed under the terms of the GPLv2+ open source
licence. Each component (which uSWID calls an “identity”) can have as many interconnections as
needed, linking together the libpng component it requires to function, and also the compiler used
to build it.

To identify each component we need two things – an ID – which allows us to cross-link the component
from other components, and also a version.
I think we should all get a lot better about versioning components using semantic versions – and
also bumping the major/minor/micro numbers much more frequently.
This makes the SBoM more interesting, and more importantly makes the security analysis and VEX
tagging possible in the future. We also need to be strict about namespacing, e.g. if the AMI
`CryptoDxe.efi` is a different thing from the EDK2 `CryptoDxe.efi` then either the former or latter
needs an identifier, e.g. using the “persistent ID” in uSWID nomenclature of something like
`com.ami` or `com.intel`.

In some cases the ID of the component (the SWID identity) is already in a nice GUID form – for
instance using the UEFI GUID defined in an official specification.
In other cases like gcc (where we have no UUID defined) I’ve just used a `UUID5(DNS,“gcc”)` – so we
get a nice GUID that we can link within the object and that compiles down to a 128 bit number in coSWID.

Helpfully, we already have some of this information in EDK2 in the form of `.inf files` – we
certainly need additional data – but using these files can be a really good start. e.g. we can
munge something like this:

    [Defines]
      BASE_NAME                  	= CryptoDxe
      FILE_GUID                  	= 2119BBD7-9432-4f47-B5E2-5C4EA31B6BDC
      VERSION_STRING             	= 1.0
    [Sources]
      CryptoDxe.c
      CryptoDxe.h
    [LibraryClasses]
      BaseMemoryLib
      HobLib

…and then generate a lot of the needed SBoM data automatically. It doesn’t tell us about any
entities (the *who*, which we’ll need to actually research and add for each module) but we can add
a lot of extra detail automatically.
For example the tree hash, aka the “git describe” SHA1 which uSWID refers to as the “edition”, and
the `SHA1(CryptoDxe.c+CryptoDxe.h)`, aka the “file hash” or as uSWID calls it the “colloquial version”.

I’m not very familiar with the AMI, Insyde and Phoenix internal build tools (for obvious reasons)
but I figured an example might be worth an [additional] thousand words.
I’ve uploaded a tiny example which uses the meson build system – which is just something I’m
familiar with – any build system that can chain rules “run X on file Y to make file Z” could be
made to work too.

The general idea is that each module (e.g. a DXE) would build a `.ini` file from the existing `.inf`
file – and then the auto-converted `.ini`, a per-module `supplemental.ini` and a per-project
`toplevel.ini` would be combined into a per-module `.uswid` container.
Once all the modules have been built, all the temporary `.uswid` files would be squashed together
along with any static data helpfully provided by the silicon vendors.
My example has Intel providing a static JSON file (showing that the format is unimportant, the
data is what we need) that’s packaged with the microcode.
It’s fictitious, but maybe it’s what we can ask Intel for in the future.

To build the demo and show the resulting file you can do:

    pip install uswid
    meson configure build
    ninja -C build
    uswid --load build/demo.uswid --verbose

Which gives:

    Saving:
    uSwidIdentity(tag_id="2119bbd7-9432-4f47-b5e2-5c4ea31b6bdc",tag_version="0",software_name="CryptoDxe",software_version="1.0"):
     - uSwidLink(rel="see-also",href="swid:8ba86535-adc9-51d4-a88d-852cfe14c8cd")
     - uSwidLink(rel="see-also",href="swid:a3a5334f-2644-590b-a768-5f2f54077537")
     - uSwidEntity(regid="com.intel",name="Intel",roles=SOFTWARE_CREATOR)
     - uSwidEntity(regid="com.odm",name="ODM",roles=TAG_CREATOR)
     - uSwidEntity(regid="com.oem",name="OEM",roles=DISTRIBUTOR)
     - uSwidPayload(name="CryptoDxe.efi",size=24184)
     - uSwidHash(alg_id=SHA256,value="4e28869c26589e2ced2dcdeb71e834d55db1961be48fe6c16937b59518b0ffc0")
     - uSwidEvidence(date="2023-10-06 16:09:14.629390",device_id=hughsie-work)
    uSwidIdentity(tag_id="f43cae5a-baea-5023-bc90-3a83cd4785cc",tag_version="0",software_name="gcc",software_version="13.2.1"):
     - uSwidEntity(regid="org.gnu",name="GNU Project",roles=SOFTWARE_CREATOR,TAG_CREATOR)
    uSwidIdentity(tag_id="bcbd84ff-9898-4922-8ade-dd4bbe2e40ba",tag_version="0",software_name="MCU 06-03-02",software_version="20230808"):
     - uSwidEntity(regid="com.intel",name="Intel Corporation",roles=TAG_CREATOR,SOFTWARE_CREATOR)
     - uSwidPayload(name="intel-ucode-06-03-02",size=12)
     - uSwidHash(alg_id=SHA256,value="a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447")
     - uSwidEvidence(date="2023-09-15 12:34:56",device_id=None)
    uSwidIdentity(tag_id="b84ed8ed-a7b1-502f-83f6-90132e68adef",tag_version="0",software_name="fwupdx64",software_version="1.5"):
     - uSwidLink(rel="license",href="https://spdx.org/licenses/LGPL-2.0.html")
     - uSwidEntity(regid="hughsie.com",name="Richard Hughes",roles=MAINTAINER,TAG_CREATOR)
    uSwidIdentity(tag_id="21242ff8-e2c6-5801-a4f3-807acc08a2d2",tag_version="0",software_name="ModemBaseband",software_version="11.22.33"):
     - uSwidEntity(regid="hughski.com",name="Hughski Limited",roles=TAG_CREATOR,DISTRIBUTOR,SOFTWARE_CREATOR)

The output `demo.uswid` is 842 bytes in size.
