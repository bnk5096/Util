import os
import json
import sys

repos = {'tomcat': ['.bat', '.bmp', '.bnd', '.br', '.class', '.classpath', '.ContainerProvider', '.css', '.default', '.dia', '.dtd', '.html', '.idx', '.iml', '.java', '.jj', '.jjt', '.jks', '.json', '.jsp', '.jspf', '.jspx', '.launch', '.license', '.manifest', '.md', '.MF', '.nsi', '.pack', '.pem', '.pl', '.policy', '.pom', '.project', '.properties', '.Dockerfile', '.sample', '.sh', '.shtml', '.svg', '.tag', '.tagx', '.tasks', '.tld', '.txt', '.woff', '.xhtml', '.xml', '.xsd', '.xsl'], 
        'django': ['bat', 'cfg', 'conf', 'css', 'dbf', 'djtpl', 'dot-file', 'egg', 'eml', 'eot', 'geojson', 'gitattributes', 'gitignore', 'gitkeep', 'graffle', 'hidden', 'html', 'ico', 'idx', 'in', 'ini', 'js', 'json', 'kml', 'Makefile', 'md', 'mo', 'po', 'pristine', 'prj', 'py', 'py-tpl', 'python', 'rst', 'sample', 'sh', 'shp', 'shx', 'svg', 'thtml', 'tpl', 'ttf', 'txt', 'TXT', 'unkn', 'unknown', 'vrt', 'woff', 'woff2', 'x', 'xml', 'yml'], 
        'FFmpeg': ['Makefile', 'S', 'asm', 'awk', 'bisect-create', 'c', 'cl', 'cl2c', 'clean-diff', 'makedef', 'mslink', 'configure', 'cpp', 'css', 'cu', 'cuh', 'dpx', 'dvd2concat', 'example', 'ffconcat', 'ffmeta', 'ffpreset', 'Makefile', 'fits', 'gen-rc', 'h', 'html', 'idx', 'init', 'libav-merge-next-commit', 'list', 'm', 'mailmap', 'mak', 'make_chlayout_test', 'md', 'missing_codec_desc', 'murge', 'pam', 'patcheck', 'pl', 'plotframes', 'pm', 'png', 'pnm', 'py', 'rb', 'rc', 'sample', 'sh', 'supp', 'template', 'texi', 'txt', 'unwrap-diff', 'v', 'voc', 'xsd', 'xwd', 'yml'], 
        'httpd': ['makefile', 'Makefile', '.awk', '.buildconf', '.c', '.cmake', '.cocci', '.conf', '.css', '.d', '.def', '.dsp', '.dtd', '.h', '.in', '.inc', '.js', '.ksh', '.ldap', '.lua', '.m4', '.manifest', '.mk', '.perl', '.pl', '.pro', '.properties', '.ps', '.py', '.rc', '.sh', '.tr', '.vbs', '.win', '.xml', '.xsl', '.y', '.yml'], 
        'struts': ['.cfg', '.cmd', '.css', '.dtd', '.eot', '.ftl', '.gdsl', '.html', '.idx', '.java', 'Jenkinsfile', '.jjt', '.jrxml', '.js', '.jsp', '.map', '.md', '.mvnw', '.pack', '.properties', '.sample', '.svg', '.tld', '.ttf', '.txt', '.vm', '.woff', '.woff2', '.xml', '.xsl', '.yaml', '.yml'], 
        'systemd': ['.h', '.c', '.sh', 'Makefile', 'SKELETON', '.arch', '.automount', '.awk', '.build', '.c', '.catalog', '.clang-format', '.cocci', '.conf', '.configure', '.css', '.ctags', '.dict', '.disabled', '.el', '.example', '.expected-err', '.expected-group', '.expected-passwd', '.fc', '.gperf', '.h', '.hwdb'], 
        'linux': ['Rakefile', '.a', '.aac', '.abc', '.ac', '.ac3', '.adm', '.adts', '.aff', '.ai', '.aidl', '.aif', '.aiff', '.am', '.amd64', '.amr', '.ani', '.antlr', '.apk', '.app', '.args', '.arj', '.arm', '.arm64', '.asciipb', '.asf', '.asis', '.asm', '.attr', '.avi', '.awk', '.babelrc', '.bat', '.bazel', '.bc', '.bcb', '.bdic', '.beg', '.begin', '.bgra', '.bin', '.BIN', '.bmp', '.bowerrc', '.br', '.bsdiff', 'BUILD', '.bz2', '.bzl', '.c', '.cab', '.cbor', '.cc', '.cer', '.cfg', '.cgi', '.clang-tidy', '.class', '.classes', '.classpath', '.cmake', '.cmd', '.cmx', '.cnf', '.code2flow', '.coffee', '.conf', '.config', '.content', '.context', '.cp', '.cpio', '.cpp', '.crashpad', '.crl', '.croc', '.cron', '.crossfile', '.crt', '.crx', '.crx2', '.crx3', '.cs', '.csproj', '.csr', '.css', '.css_t', '.csv', '.cti', '.cur', '.cxx', '.dart', '.dat', '.data', '.db', '.deb', '.def', '.defs', '.der', '.dex', '.dic', '.dict', '.diff', '.dirs', '.disable', '.dislocator', '.dj', '.dll', '.dm', '.dmg', '.doc', '.dot', '.dox', '.doxy', '.draft', '.dsc', '.dsp', '.dsw', '.dtd', '.dummy', '.dump', '.eac3', '.ejs', '.el', '.elm', '.ember-cli', '.emf', '.empty', '.end', '.ent', '.eot', '.eps', '.es', '.excludes', '.exe', '.expected', '.explain', '.export', '.exports', '.ext', '.extjs', '.fake', '.fallback', '.fbs', '.fea', '.fidl', '.filter', '.filters', '.first', '.flac', '.flags', '.flv', '.foo', '.fragment', '.g', '.gdb', '.gemspec', '.glif', '.gn', '.gni', '.go', '.golden', '.good', '.gpd', '.gperf', '.gpg', '.gradle', '.grd', '.grdp', '.groovy', '.gtestjs', '.guess', '.gyp', '.gypi', '.gz', '.gzip', '.h', '.handlebars', '.hashes', '.hbs', '.header', '.headers', '.hevc', '.hidden', '.hlsl', '.hml', '.lnk', '.log', '.lrz', '.lst', '.lz', '.lzma', '.lzo', '.m', '.m2ts', '.m32', '.m3u8', '.m4', '.m4a', '.make', 'Makefiles', '.mako', '.man', '.manifest', '.manpages', '.map', '.mc', '.md', '.menu', '.mht', '.mhtml', '.mingw', '.mips', '.mips64el', '.mipsel', '.mjs', '.mk', '.mkv', '.mm', '.mojom', '.mojomsg', '.mon', '.morph', '.msc', '.msg', '.msvc', '.myspell', '.myt', '.n', '.natvis', '.nc', '.nexe', '.nib', '.ninja', '.nmake', '.nmf', '.not-css', '.not-html', '.notpy', '.npmignore', '.nsproxy', '.nuspec', '.odt', '.oga', '.ogg', '.ogv', '.old', '.onc', '.options', '.opus', '.order', '.orf', '.otf', '.out', '.output', '.pam', '.patch', '.pb', '.pb_text', '.pch', '.pcm', '.pddm', '.pdf', '.pdl', '.pem', '.pfx', '.pgm', '.php', '.pidl', '.pins', '.pk8', '.pkg', '.pkgproj', '.pkpass', '.pl', '.plist', '.pltsuite', '.podspec', '.pol', '.polymer', '.Processor', '.proctype', '.prop', '.properties', '.props', '.proto', '.ps1', '.pump', '.pvk', '.pwg', '.py', '.pyd', '.pydeps', '.pyl', '.py-str', '.qemu', '.rar', '.rb', '.rc', '.rdf', '.release', '.resx', '.rgs', '.rm', '.rpc', '.rules', '.ruleset', '.rz', '.s', '.S', '.sample', '.sb', '.scons', '.scss', '.sct', '.sctlist', '.sdef', '.security', '.sed', '.see_also', '.settings', '.sh', '.sitx', '.skeletons', '.sln', '.snk', '.so', '.spc', '.spec', '.sql', '.sqlite', '.src', '.sst', '.status', '.storyboard', '.strings', '.sub', '.subtest', '.sug', '.swf', '.swift', '.sxg', '.sym', '.syms', '.syntax', '.tab', '.tar', '.tcl', '.templ', '.template', '.terms', '.test', '.testcases', '.test-mojom', '.tests', '.text', '.textpb', '.textproto', '.tlb', '.tmpl', '.tokencap', '.tokenizers', '.toml', '.ts', '.ttc', '.ttx', '.txt', '.TXT', '.typemap', '.types', '.unitjs', '.unix', '.usdz', '.vanilla', '.ver', '.version', '.visualizer', '.vpython', '.vsct', '.vsix', '.vtt', '.vue', '.wasm', '.wat', '.wbn', '.webarchive', '.whitelist', '.woff', '.woff2', '.wrong', '.wxs', '.xaml', '.xcf', '.xht', '.xhtml', '.xib', '.xls', '.xmb', '.xml', '.xpm', '.xsd', '.xsl', '.xslt', '.xtb', '.xul', '.xz', '.y', '.yaml', '.yapf', '.yml', '.yuv', '.Z', '.zoneinfo', '.zoo', '.zOS', '.ztf', '.zuc', '.zzz'],
        'chromium': ['Rakefile', '.a', '.aac', '.abc', '.ac', '.ac3', '.adm', '.adts', '.aff', '.ai', '.aidl', '.aif', '.aiff', '.am', '.amd64', '.amr', '.ani', '.antlr', '.apk', '.app', '.args', '.arj', '.arm', '.arm64', '.asciipb', '.asf', '.asis', '.asm', '.attr', '.avi', '.awk', '.babelrc', '.bat', '.bazel', '.bc', '.bcb', '.bdic', '.beg', '.begin', '.bgra', '.bin', '.BIN', '.bmp', '.bowerrc', '.br', '.bsdiff', 'BUILD', '.bz2', '.bzl', '.c', '.cab', '.cbor', '.cc', '.cer', '.cfg', '.cgi', '.clang-tidy', '.class', '.classes', '.classpath', '.cmake', '.cmd', '.cmx', '.cnf', '.code2flow', '.coffee', '.conf', '.config', '.content', '.context', '.cp', '.cpio', '.cpp', '.crashpad', '.crl', '.croc', '.cron', '.crossfile', '.crt', '.crx', '.crx2', '.crx3', '.cs', '.csproj', '.csr', '.css', '.css_t', '.csv', '.cti', '.cur', '.cxx', '.dart', '.dat', '.data', '.db', '.deb', '.def', '.defs', '.der', '.dex', '.dic', '.dict', '.diff', '.dirs', '.disable', '.dislocator', '.dj', '.dll', '.dm', '.dmg', '.doc', '.dot', '.dox', '.doxy', '.draft', '.dsc', '.dsp', '.dsw', '.dtd', '.dummy', '.dump', '.eac3', '.ejs', '.el', '.elm', '.ember-cli', '.emf', '.empty', '.end', '.ent', '.eot', '.eps', '.es', '.excludes', '.exe', '.expected', '.explain', '.export', '.exports', '.ext', '.extjs', '.fake', '.fallback', '.fbs', '.fea', '.fidl', '.filter', '.filters', '.first', '.flac', '.flags', '.flv', '.foo', '.fragment', '.g', '.gdb', '.gemspec', '.glif', '.gn', '.gni', '.go', '.golden', '.good', '.gpd', '.gperf', '.gpg', '.gradle', '.grd', '.grdp', '.groovy', '.gtestjs', '.guess', '.gyp', '.gypi', '.gz', '.gzip', '.h', '.handlebars', '.hashes', '.hbs', '.header', '.headers', '.hevc', '.hidden', '.hlsl', '.hml', '.lnk', '.log', '.lrz', '.lst', '.lz', '.lzma', '.lzo', '.m', '.m2ts', '.m32', '.m3u8', '.m4', '.m4a', '.make', 'Makefiles', '.mako', '.man', '.manifest', '.manpages', '.map', '.mc', '.md', '.menu', '.mht', '.mhtml', '.mingw', '.mips', '.mips64el', '.mipsel', '.mjs', '.mk', '.mkv', '.mm', '.mojom', '.mojomsg', '.mon', '.morph', '.msc', '.msg', '.msvc', '.myspell', '.myt', '.n', '.natvis', '.nc', '.nexe', '.nib', '.ninja', '.nmake', '.nmf', '.not-css', '.not-html', '.notpy', '.npmignore', '.nsproxy', '.nuspec', '.odt', '.oga', '.ogg', '.ogv', '.old', '.onc', '.options', '.opus', '.order', '.orf', '.otf', '.out', '.output', '.pam', '.patch', '.pb', '.pb_text', '.pch', '.pcm', '.pddm', '.pdf', '.pdl', '.pem', '.pfx', '.pgm', '.php', '.pidl', '.pins', '.pk8', '.pkg', '.pkgproj', '.pkpass', '.pl', '.plist', '.pltsuite', '.podspec', '.pol', '.polymer', '.Processor', '.proctype', '.prop', '.properties', '.props', '.proto', '.ps1', '.pump', '.pvk', '.pwg', '.py', '.pyd', '.pydeps', '.pyl', '.py-str', '.qemu', '.rar', '.rb', '.rc', '.rdf', '.release', '.resx', '.rgs', '.rm', '.rpc', '.rules', '.ruleset', '.rz', '.s', '.S', '.sample', '.sb', '.scons', '.scss', '.sct', '.sctlist', '.sdef', '.security', '.sed', '.see_also', '.settings', '.sh', '.sitx', '.skeletons', '.sln', '.snk', '.so', '.spc', '.spec', '.sql', '.sqlite', '.src', '.sst', '.status', '.storyboard', '.strings', '.sub', '.subtest', '.sug', '.swf', '.swift', '.sxg', '.sym', '.syms', '.syntax', '.tab', '.tar', '.tcl', '.templ', '.template', '.terms', '.test', '.testcases', '.test-mojom', '.tests', '.text', '.textpb', '.textproto', '.tlb', '.tmpl', '.tokencap', '.tokenizers', '.toml', '.ts', '.ttc', '.ttx', '.txt', '.TXT', '.typemap', '.types', '.unitjs', '.unix', '.usdz', '.vanilla', '.ver', '.version', '.visualizer', '.vpython', '.vsct', '.vsix', '.vtt', '.vue', '.wasm', '.wat', '.wbn', '.webarchive', '.whitelist', '.woff', '.woff2', '.wrong', '.wxs', '.xaml', '.xcf', '.xht', '.xhtml', '.xib', '.xls', '.xmb', '.xml', '.xpm', '.xsd', '.xsl', '.xslt', '.xtb', '.xul', '.xz', '.y', '.yaml', '.yapf', '.yml', '.yuv', '.Z', '.zoneinfo', '.zoo', '.zOS', '.ztf', '.zuc', '.zzz']
        } 


class Alias:
    
    def __init__(self, name):
        self.name = name
        if "test" in name.lower():
            self.test = True
        else:
            self.test = False
        self.off = False
        self.aliases = []
        self.aliases.append(name)
    
    def add_alias(self, alias):
        self.aliases.append(alias)

    def set_off(self):
        self.off = True


def main():
    for repo in [sys.argv[1]]:
        # Run the requests to get all the files
        # os.system("git -C " + repo + " log --stat --name-only --pretty='' | uniq  > " + repo + "_out.txt")
        # Read the output file and filter it down to only valid extensions
        data = {}
        with open("file_data/" + repo + "_out.txt") as f:
            for line in f:
                for ending in repos[repo]:
                    if line.strip().endswith(ending):
                        data[line.strip()] = []
                        break

        # Remove the tests from consideration (Prior way of doing this)
        # to_remove = []
        # for df in data:
        #     if "test" in df:
        #         to_remove.append(df)
        #         continue
        #     for alias in data[df]:
        #         if "test" in alias:
        #             to_remove.append(df)
        #             break
        # for item in to_remove:
        #     data.pop(item)
    
        # pass # Run the alias checking // renames
        aliases = []
        for df in data:
            if data[df] != []:
                continue
            # print(df)
            os.system("git -C " + "Repos/"+ repo + " log --stat --name-only --follow --pretty='' -- \"" + df + "\" > " + repo +"_temp.txt")
            aliases_temp = set()
            with open(repo + "_temp.txt") as f:
                for line in f:
                    aliases_temp.add(line.strip())
            os.system("rm " + repo +"_temp.txt")
            temp_node = Alias(df)
            for item in aliases_temp:
                if item not in temp_node.aliases:
                    temp_node.add_alias(item)
            data[df] = temp_node
            for al in aliases_temp:
                if al not in data:
                    print("Excluded file in aliases:", al)
                    print("Source file:", df)
                    continue
                    # print("Dict: ", data)
                data[al] = temp_node
            aliases.append(temp_node)






        # for df in data:
        #     out = subprocess.check_output("git", "-C", repo, "log", "--stat", "--name-only", "--follow", "--pretty='", "--", df)
        #     aliases = []
        #     # figure out the renames
        #     data[df] = aliases


        # get the VHP data.
        of_interest_filtered = []
        with open("vhp_files_out.json") as f:
            vhp_data = json.load(f)
            of_interest = vhp_data[repo]
            for entry in of_interest:
                # if "test" in entry:
                #     of_interest.remove(entry)
                #     continue
                for ending in repos[repo]:
                    if entry.endswith(ending):
                        of_interest_filtered.append(entry)
                        break
        
        # Count util files, count non-util files
        # names = set()
        # for entry in data:
        #     names.add(entry)
        # for entry in data:
        #     for alias in data[entry]:
        #         names.remove(alias)

        for name in of_interest_filtered:
            if name not in data:
                # print(name)
                continue
            data[name].set_off()

        util = []
        util_c = 0
        non_util = []
        non_util_c = 0

        util_off = []
        util_c_off = 0
        non_util_off = []
        non_util_c_off = 0

        for node in aliases:
            if node.off:
                if "util" in node.name.lower() or "helper" in node.name.lower():
                    util_off.append(node)
                    util_c_off += 1
                else:
                    non_util_off.append(node)
                    non_util_c_off += 1
            else:
                if "util" in node.name.lower() or "helper" in node.name.lower():
                    util.append(node)
                    util_c += 1
                else:
                    non_util.append(node)
                    non_util_c += 1


        # Calculate odds radtio & Output it along with raw numbers in the calculations
        print("Project:", repo)
        print("Overall valid extensions - Tests Included")
        print((util_c_off/(util_c-util_c_off))/(non_util_c_off/(non_util_c - non_util_c_off)))
        print("Total Non-Util Files:", non_util_c)
        print("Total Util Files:", util_c)
        print("Util Offenders:", util_c_off)
        print("Non-Util Offenders:", non_util_c_off)


        # Do it again with tests gone
        util = []
        util_c = 0
        non_util = []
        non_util_c = 0
        util_off = []
        util_c_off = 0
        non_util_off = []
        non_util_c_off = 0

        for node in aliases:
            if node.test:
                continue
            if node.off:
                if "util" in node.name.lower() or "helper" in node.name.lower():
                    util_off.append(node)
                    util_c_off += 1
                else:
                    non_util_off.append(node)
                    non_util_c_off += 1
            else:
                if "util" in node.name.lower() or "helper" in node.name.lower():
                    util.append(node)
                    util_c += 1
                else:
                    non_util.append(node)
                    non_util_c += 1
        print("Overall valid extensions - Tests Excluded")
        print((util_c_off/(util_c-util_c_off))/(non_util_c_off/(non_util_c - non_util_c_off)))
        print("Total Non-Util Files:", non_util_c)
        print("Total Util Files:", util_c)
        print("Util Offenders:", util_c_off)
        print("Non-Util Offenders:", non_util_c_off)


        # By Language
        
        for ending in repos[repo]:
            util = []
            util_c = 0
            non_util = []
            non_util_c = 0

            util_off = []
            util_c_off = 0
            non_util_off = []
            non_util_c_off = 0

            for node in aliases:
                if not node.name.endswith(ending):
                    continue
                if node.off:
                    if "util" in node.name.lower() or "helper" in node.name.lower():
                        util_off.append(node)
                        util_c_off += 1
                    else:
                        non_util_off.append(node)
                        non_util_c_off += 1
                else:
                    if "util" in node.name.lower() or "helper" in node.name.lower():
                        util.append(node)
                        util_c += 1
                    else:
                        non_util.append(node)
                        non_util_c += 1


            # Calculate odds radtio & Output it along with raw numbers in the calculations
            print("Extension:", ending, "Tests Included")
            try:
                print((util_c_off/(util_c-util_c_off))/(non_util_c_off/(non_util_c - non_util_c_off)))
            except:
                print("Math Error")
            print("Total Non-Util Files:", non_util_c)
            print("Total Util Files:", util_c)
            print("Util Offenders:", util_c_off)
            print("Non-Util Offenders:", non_util_c_off)

            # Do it again with tests gone
            util = []
            util_c = 0
            non_util = []
            non_util_c = 0
            util_off = []
            util_c_off = 0
            non_util_off = []
            non_util_c_off = 0

            for node in aliases:
                if not node.name.endswith(ending):
                    continue
                if node.test:
                    continue
                if node.off:
                    if "util" in node.name.lower() or "helper" in node.name.lower():
                        util_off.append(node)
                        util_c_off += 1
                    else:
                        non_util_off.append(node)
                        non_util_c_off += 1
                else:
                    if "util" in node.name.lower() or "helper" in node.name.lower():
                        util.append(node)
                        util_c += 1
                    else:
                        non_util.append(node)
                        non_util_c += 1
            
            print("Extension:", ending, "Tests Excluded")
            try:
                print((util_c_off/(util_c-util_c_off))/(non_util_c_off/(non_util_c - non_util_c_off)))
            except:
                print("Math Error")
            print("Total Non-Util Files:", non_util_c)
            print("Total Util Files:", util_c)
            print("Util Offenders:", util_c_off)
            print("Non-Util Offenders:", non_util_c_off)

            




if __name__ == '__main__':
    main()
