project('firmware', 'c', version: '0.0.1')

cc = meson.get_compiler('c')

git = find_program('git')
source_version = run_command([git, 'describe'], check: false).stdout().strip()

conf = configuration_data()
conf.set('COMPILER_NAME', cc.get_id())
conf.set('COMPILER_VERSION', cc.version())

# this is a list of generated or static uSWID files
sbom_built = []
sbom_static = []

# find the binary
uswid = find_program('uswid')

# add a compiler entity so we know what we build this with
sbom_static += configure_file(
  input : 'compiler.ini',
  output : 'compiler.ini',
  configuration : conf,
)

# we import this into EVERY BUILT SBoM component to override values
ini_toplevel = configure_file(
  input : 'toplevel.ini',
  output : 'toplevel.ini',
  configuration : conf,
)

# this is used by multiple UEFI modules
inf2ini = ['python3', files('inf2ini.py')]

#sbom_built += custom_target('compiler.uswid',
#  input: ini_compiler,
#  output: 'compiler.uswid',
#  command: [uswid, '--verbose', '--load', '@INPUT@', '--save', '@OUTPUT@'],
#)

subdir('src')
subdir('ucode')
subdir('parachuted')

# build all the small per-component uSWID files into one tiny deduped and compressed blob
args = []
foreach uswid_file: sbom_built
  args += [uswid_file.full_path()]
endforeach
foreach uswid_file: sbom_static
  args += [uswid_file]
endforeach
uswid_blob = custom_target('demo.uswid',
  depends: sbom_built,
  output: 'demo.uswid',
  command: [uswid, '--verbose', '--compress', '--load', args, '--save', '@OUTPUT@'],
  build_by_default: true,
)
