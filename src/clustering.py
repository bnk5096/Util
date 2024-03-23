import os
import pathlib


repos = {'tomcat': ['.bat', '.bmp', '.bnd', '.br', '.class', '.classpath', '.ContainerProvider', '.css', '.default', '.dia', '.dtd', '.html', '.idx', '.iml', '.java', '.jj', '.jjt', '.jks', '.json', '.jsp', '.jspf', '.jspx', '.launch', '.license', '.manifest', '.md', '.MF', '.nsi', '.pack', '.pem', '.pl', '.policy', '.pom', '.project', '.properties', '.Dockerfile', '.sample', '.sh', '.shtml', '.svg', '.tag', '.tagx', '.tasks', '.tld', '.txt', '.woff', '.xhtml', '.xml', '.xsd', '.xsl'], 
         'django': ['bat', 'cfg', 'conf', 'css', 'dbf', 'djtpl', 'dot-file', 'egg', 'eml', 'eot', 'geojson', 'gitattributes', 'gitignore', 'gitkeep', 'graffle', 'hidden', 'html', 'ico', 'idx', 'in', 'ini', 'js', 'json', 'kml', 'Makefile', 'md', 'mo', 'po', 'pristine', 'prj', 'py', 'py-tpl', 'python', 'rst', 'sample', 'sh', 'shp', 'shx', 'svg', 'thtml', 'tpl', 'ttf', 'txt', 'TXT', 'unkn', 'unknown', 'vrt', 'woff', 'woff2', 'x', 'xml', 'yml'], 
         'FFmpeg': ['Makefile', 'S', 'asm', 'awk', 'bisect-create', 'c', 'cl', 'cl2c', 'clean-diff', 'makedef', 'mslink', 'configure', 'cpp', 'css', 'cu', 'cuh', 'dpx', 'dvd2concat', 'example', 'ffconcat', 'ffmeta', 'ffpreset', 'Makefile', 'fits', 'gen-rc', 'h', 'html', 'idx', 'init', 'libav-merge-next-commit', 'list', 'm', 'mailmap', 'mak', 'make_chlayout_test', 'md', 'missing_codec_desc', 'murge', 'pam', 'patcheck', 'pl', 'plotframes', 'pm', 'png', 'pnm', 'py', 'rb', 'rc', 'sample', 'sh', 'supp', 'template', 'texi', 'txt', 'unwrap-diff', 'v', 'voc', 'xsd', 'xwd', 'yml'], 
         'httpd': ['makefile', 'Makefile', '.awk', '.buildconf', '.c', '.cmake', '.cocci', '.conf', '.css', '.d', '.def', '.dsp', '.dtd', '.h', '.in', '.inc', '.js', '.ksh', '.ldap', '.lua', '.m4', '.manifest', '.mk', '.perl', '.pl', '.pro', '.properties', '.ps', '.py', '.rc', '.sh', '.tr', '.vbs', '.win', '.xml', '.xsl', '.y', '.yml'], 
         'struts': ['.cfg', '.cmd', '.css', '.dtd', '.eot', '.ftl', '.gdsl', '.html', '.idx', '.java', 'Jenkinsfile', '.jjt', '.jrxml', '.js', '.jsp', '.map', '.md', '.mvnw', '.pack', '.properties', '.sample', '.svg', '.tld', '.ttf', '.txt', '.vm', '.woff', '.woff2', '.xml', '.xsl', '.yaml', '.yml'], 
         'systemd': ['.h', '.c', '.sh', 'Makefile', 'SKELETON', '.arch', '.automount', '.awk', '.build', '.c', '.catalog', '.clang-format', '.cocci', '.conf', '.configure', '.css', '.ctags', '.dict', '.disabled', '.el', '.example', '.expected-err', '.expected-group', '.expected-passwd', '.fc', '.gperf', '.h', '.hwdb'], 
         'linux': ['Rakefile', '.a', '.aac', '.abc', '.ac', '.ac3', '.adm', '.adts', '.aff', '.ai', '.aidl', '.aif', '.aiff', '.am', '.amd64', '.amr', '.ani', '.antlr', '.apk', '.app', '.args', '.arj', '.arm', '.arm64', '.asciipb', '.asf', '.asis', '.asm', '.attr', '.avi', '.awk', '.babelrc', '.bat', '.bazel', '.bc', '.bcb', '.bdic', '.beg', '.begin', '.bgra', '.bin', '.BIN', '.bmp', '.bowerrc', '.br', '.bsdiff', 'BUILD', '.bz2', '.bzl', '.c', '.cab', '.cbor', '.cc', '.cer', '.cfg', '.cgi', '.clang-tidy', '.class', '.classes', '.classpath', '.cmake', '.cmd', '.cmx', '.cnf', '.code2flow', '.coffee', '.conf', '.config', '.content', '.context', '.cp', '.cpio', '.cpp', '.crashpad', '.crl', '.croc', '.cron', '.crossfile', '.crt', '.crx', '.crx2', '.crx3', '.cs', '.csproj', '.csr', '.css', '.css_t', '.csv', '.cti', '.cur', '.cxx', '.dart', '.dat', '.data', '.db', '.deb', '.def', '.defs', '.der', '.dex', '.dic', '.dict', '.diff', '.dirs', '.disable', '.dislocator', '.dj', '.dll', '.dm', '.dmg', '.doc', '.dot', '.dox', '.doxy', '.draft', '.dsc', '.dsp', '.dsw', '.dtd', '.dummy', '.dump', '.eac3', '.ejs', '.el', '.elm', '.ember-cli', '.emf', '.empty', '.end', '.ent', '.eot', '.eps', '.es', '.excludes', '.exe', '.expected', '.explain', '.export', '.exports', '.ext', '.extjs', '.fake', '.fallback', '.fbs', '.fea', '.fidl', '.filter', '.filters', '.first', '.flac', '.flags', '.flv', '.foo', '.fragment', '.g', '.gdb', '.gemspec', '.glif', '.gn', '.gni', '.go', '.golden', '.good', '.gpd', '.gperf', '.gpg', '.gradle', '.grd', '.grdp', '.groovy', '.gtestjs', '.guess', '.gyp', '.gypi', '.gz', '.gzip', '.h', '.handlebars', '.hashes', '.hbs', '.header', '.headers', '.hevc', '.hidden', '.hlsl', '.hml', '.lnk', '.log', '.lrz', '.lst', '.lz', '.lzma', '.lzo', '.m', '.m2ts', '.m32', '.m3u8', '.m4', '.m4a', '.make', 'Makefiles', '.mako', '.man', '.manifest', '.manpages', '.map', '.mc', '.md', '.menu', '.mht', '.mhtml', '.mingw', '.mips', '.mips64el', '.mipsel', '.mjs', '.mk', '.mkv', '.mm', '.mojom', '.mojomsg', '.mon', '.morph', '.msc', '.msg', '.msvc', '.myspell', '.myt', '.n', '.natvis', '.nc', '.nexe', '.nib', '.ninja', '.nmake', '.nmf', '.not-css', '.not-html', '.notpy', '.npmignore', '.nsproxy', '.nuspec', '.odt', '.oga', '.ogg', '.ogv', '.old', '.onc', '.options', '.opus', '.order', '.orf', '.otf', '.out', '.output', '.pam', '.patch', '.pb', '.pb_text', '.pch', '.pcm', '.pddm', '.pdf', '.pdl', '.pem', '.pfx', '.pgm', '.php', '.pidl', '.pins', '.pk8', '.pkg', '.pkgproj', '.pkpass', '.pl', '.plist', '.pltsuite', '.podspec', '.pol', '.polymer', '.Processor', '.proctype', '.prop', '.properties', '.props', '.proto', '.ps1', '.pump', '.pvk', '.pwg', '.py', '.pyd', '.pydeps', '.pyl', '.py-str', '.qemu', '.rar', '.rb', '.rc', '.rdf', '.release', '.resx', '.rgs', '.rm', '.rpc', '.rules', '.ruleset', '.rz', '.s', '.S', '.sample', '.sb', '.scons', '.scss', '.sct', '.sctlist', '.sdef', '.security', '.sed', '.see_also', '.settings', '.sh', '.sitx', '.skeletons', '.sln', '.snk', '.so', '.spc', '.spec', '.sql', '.sqlite', '.src', '.sst', '.status', '.storyboard', '.strings', '.sub', '.subtest', '.sug', '.swf', '.swift', '.sxg', '.sym', '.syms', '.syntax', '.tab', '.tar', '.tcl', '.templ', '.template', '.terms', '.test', '.testcases', '.test-mojom', '.tests', '.text', '.textpb', '.textproto', '.tlb', '.tmpl', '.tokencap', '.tokenizers', '.toml', '.ts', '.ttc', '.ttx', '.txt', '.TXT', '.typemap', '.types', '.unitjs', '.unix', '.usdz', '.vanilla', '.ver', '.version', '.visualizer', '.vpython', '.vsct', '.vsix', '.vtt', '.vue', '.wasm', '.wat', '.wbn', '.webarchive', '.whitelist', '.woff', '.woff2', '.wrong', '.wxs', '.xaml', '.xcf', '.xht', '.xhtml', '.xib', '.xls', '.xmb', '.xml', '.xpm', '.xsd', '.xsl', '.xslt', '.xtb', '.xul', '.xz', '.y', '.yaml', '.yapf', '.yml', '.yuv', '.Z', '.zoneinfo', '.zoo', '.zOS', '.ztf', '.zuc', '.zzz'],
         'chromium': ['Rakefile', '.a', '.aac', '.abc', '.ac', '.ac3', '.adm', '.adts', '.aff', '.ai', '.aidl', '.aif', '.aiff', '.am', '.amd64', '.amr', '.ani', '.antlr', '.apk', '.app', '.args', '.arj', '.arm', '.arm64', '.asciipb', '.asf', '.asis', '.asm', '.attr', '.avi', '.awk', '.babelrc', '.bat', '.bazel', '.bc', '.bcb', '.bdic', '.beg', '.begin', '.bgra', '.bin', '.BIN', '.bmp', '.bowerrc', '.br', '.bsdiff', 'BUILD', '.bz2', '.bzl', '.c', '.cab', '.cbor', '.cc', '.cer', '.cfg', '.cgi', '.clang-tidy', '.class', '.classes', '.classpath', '.cmake', '.cmd', '.cmx', '.cnf', '.code2flow', '.coffee', '.conf', '.config', '.content', '.context', '.cp', '.cpio', '.cpp', '.crashpad', '.crl', '.croc', '.cron', '.crossfile', '.crt', '.crx', '.crx2', '.crx3', '.cs', '.csproj', '.csr', '.css', '.css_t', '.csv', '.cti', '.cur', '.cxx', '.dart', '.dat', '.data', '.db', '.deb', '.def', '.defs', '.der', '.dex', '.dic', '.dict', '.diff', '.dirs', '.disable', '.dislocator', '.dj', '.dll', '.dm', '.dmg', '.doc', '.dot', '.dox', '.doxy', '.draft', '.dsc', '.dsp', '.dsw', '.dtd', '.dummy', '.dump', '.eac3', '.ejs', '.el', '.elm', '.ember-cli', '.emf', '.empty', '.end', '.ent', '.eot', '.eps', '.es', '.excludes', '.exe', '.expected', '.explain', '.export', '.exports', '.ext', '.extjs', '.fake', '.fallback', '.fbs', '.fea', '.fidl', '.filter', '.filters', '.first', '.flac', '.flags', '.flv', '.foo', '.fragment', '.g', '.gdb', '.gemspec', '.glif', '.gn', '.gni', '.go', '.golden', '.good', '.gpd', '.gperf', '.gpg', '.gradle', '.grd', '.grdp', '.groovy', '.gtestjs', '.guess', '.gyp', '.gypi', '.gz', '.gzip', '.h', '.handlebars', '.hashes', '.hbs', '.header', '.headers', '.hevc', '.hidden', '.hlsl', '.hml', '.lnk', '.log', '.lrz', '.lst', '.lz', '.lzma', '.lzo', '.m', '.m2ts', '.m32', '.m3u8', '.m4', '.m4a', '.make', 'Makefiles', '.mako', '.man', '.manifest', '.manpages', '.map', '.mc', '.md', '.menu', '.mht', '.mhtml', '.mingw', '.mips', '.mips64el', '.mipsel', '.mjs', '.mk', '.mkv', '.mm', '.mojom', '.mojomsg', '.mon', '.morph', '.msc', '.msg', '.msvc', '.myspell', '.myt', '.n', '.natvis', '.nc', '.nexe', '.nib', '.ninja', '.nmake', '.nmf', '.not-css', '.not-html', '.notpy', '.npmignore', '.nsproxy', '.nuspec', '.odt', '.oga', '.ogg', '.ogv', '.old', '.onc', '.options', '.opus', '.order', '.orf', '.otf', '.out', '.output', '.pam', '.patch', '.pb', '.pb_text', '.pch', '.pcm', '.pddm', '.pdf', '.pdl', '.pem', '.pfx', '.pgm', '.php', '.pidl', '.pins', '.pk8', '.pkg', '.pkgproj', '.pkpass', '.pl', '.plist', '.pltsuite', '.podspec', '.pol', '.polymer', '.Processor', '.proctype', '.prop', '.properties', '.props', '.proto', '.ps1', '.pump', '.pvk', '.pwg', '.py', '.pyd', '.pydeps', '.pyl', '.py-str', '.qemu', '.rar', '.rb', '.rc', '.rdf', '.release', '.resx', '.rgs', '.rm', '.rpc', '.rules', '.ruleset', '.rz', '.s', '.S', '.sample', '.sb', '.scons', '.scss', '.sct', '.sctlist', '.sdef', '.security', '.sed', '.see_also', '.settings', '.sh', '.sitx', '.skeletons', '.sln', '.snk', '.so', '.spc', '.spec', '.sql', '.sqlite', '.src', '.sst', '.status', '.storyboard', '.strings', '.sub', '.subtest', '.sug', '.swf', '.swift', '.sxg', '.sym', '.syms', '.syntax', '.tab', '.tar', '.tcl', '.templ', '.template', '.terms', '.test', '.testcases', '.test-mojom', '.tests', '.text', '.textpb', '.textproto', '.tlb', '.tmpl', '.tokencap', '.tokenizers', '.toml', '.ts', '.ttc', '.ttx', '.txt', '.TXT', '.typemap', '.types', '.unitjs', '.unix', '.usdz', '.vanilla', '.ver', '.version', '.visualizer', '.vpython', '.vsct', '.vsix', '.vtt', '.vue', '.wasm', '.wat', '.wbn', '.webarchive', '.whitelist', '.woff', '.woff2', '.wrong', '.wxs', '.xaml', '.xcf', '.xht', '.xhtml', '.xib', '.xls', '.xmb', '.xml', '.xpm', '.xsd', '.xsl', '.xslt', '.xtb', '.xul', '.xz', '.y', '.yaml', '.yapf', '.yml', '.yuv', '.Z', '.zoneinfo', '.zoo', '.zOS', '.ztf', '.zuc', '.zzz']
        }


class Node:
    def __init__(self, name: str, parent: "Node", is_dir: bool, is_util: bool) -> "Node":
        self.name = name
        self.parent = parent
        self.is_dir = is_dir
        self.children = None
        if self.is_dir:
            self.children = []
        self.util_count = 0
        self.total_count = 0
        self.is_util = is_util or parent is not None and parent.is_util
        if self.is_util and not is_dir:
            self.util_count = 1
            self.parent.update_parent_util()
        if parent is not None:
            if not is_dir:
                self.total_count += 1
                self.parent.update_parent()
            parent.add_child(self)
        

    def update_parent_util(self) -> None:
        self.util_count += 1
        if self.parent is not None: 
            self.parent.update_parent_util()
    

    def update_parent(self) -> None:
        self.total_count += 1
        if self.parent is not None:
            self.parent.update_parent()


    def add_child(self, child: "Node") -> None:
        self.children.append(child)
    
    def print(self, existing_indent: str = "") -> None:
        if self.is_util:
            print_line = existing_indent + "*util*_" + self.name + "\tutil count: " + str(self.util_count) + "\ttotal count: " + str(self.total_count)
        else:
            print_line = existing_indent + self.name + "\tutil count: " + str(self.util_count) + "\ttotal count: " + str(self.total_count)
        print(print_line)
        if self.is_dir:
            for child in self.children:
                child.print(existing_indent + "\t")


def read_repo(project: str, root_dir: str) -> (list[str], list[str]):
    dir_paths = []
    paths = []
    for path, subdirs, files in os.walk(root_dir):
        for subdir in subdirs:
            dir_paths.append(str(pathlib.PurePath(path, subdir))[len(root_dir) + 1:].strip())
        for name in files:
            res = str(pathlib.PurePath(path, name))[len(root_dir) + 1:].strip()
            for ending in repos[project]:
                if res.strip().endswith(ending):
                    paths.append(res.strip())
    return dir_paths, paths
            

def main():
    # root_dir = Node("Project_Root", None, True, False)
    for project in repos:
        lookup = {}
        root_dir = Node(project + "_root", None, True, None)
        lookup["root"] = root_dir
        pathing = "Repos/" + project
        directories, files = read_repo(project, pathing)

        for entry in directories:
            splits = entry.split("/")
            if len(splits) == 1:
                parent = "root"
            else: 
                parent = "/".join(splits[:-1])
            name = splits[-1]
            lookup[entry] = Node(name, lookup[parent], True, True if "util" in name.lower() or "helper" in name.lower() else False)
        
        for entry in files:
            splits = entry.split("/")
            if len(splits) == 1:
                parent = "root"
            else: 
                parent = "/".join(splits[:-1])
            name = splits[-1]
            lookup[entry] = Node(name, lookup[parent], False, True if "util" in name.lower() or "helper" in name.lower() else False)
    
        print("Project: " + project)
        lookup["root"].print()
        print("\n\n")
        sorting_list = []
        for path, node in lookup.items():
            if node.total_count > 0 and node.is_dir:
                sorting_list.append((path, node))
        
        sorted_list = sorted(sorting_list, key= lambda x: (x[1].util_count, x[1].util_count/x[1].total_count), reverse=True)
        for entry in sorted_list:
            if entry[1].util_count == 0:
                break
            print(entry[0] + " - " + str(entry[1].util_count/entry[1].total_count) + "\tUtil: " + str(entry[1].util_count) + "  Total: " + str(entry[1].total_count))
        print("\n\n-----------------------------------\n\n")

if __name__ == '__main__':
    main()
