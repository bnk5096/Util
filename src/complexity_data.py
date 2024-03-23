"""
Reads the resultant data from complexity analysis and calculates any necessary statistical values for printing to the console
"""

import os
import json
import statistics
import scipy

# Collection of repos with the list of source code file names provided by the Vulnerability History Project Repository
repos = {'tomcat': ['.bat', '.bmp', '.bnd', '.br', '.class', '.classpath', '.ContainerProvider', '.css', '.default', '.dia', '.dtd', '.html', '.idx', '.iml', '.java', '.jj', '.jjt', '.jks', '.json', '.jsp', '.jspf', '.jspx', '.launch', '.license', '.manifest', '.md', '.MF', '.nsi', '.pack', '.pem', '.pl', '.policy', '.pom', '.project', '.properties', '.Dockerfile', '.sample', '.sh', '.shtml', '.svg', '.tag', '.tagx', '.tasks', '.tld', '.txt', '.woff', '.xhtml', '.xml', '.xsd', '.xsl'], 
        'django': ['bat', 'cfg', 'conf', 'css', 'dbf', 'djtpl', 'dot-file', 'egg', 'eml', 'eot', 'geojson', 'gitattributes', 'gitignore', 'gitkeep', 'graffle', 'hidden', 'html', 'ico', 'idx', 'in', 'ini', 'js', 'json', 'kml', 'Makefile', 'md', 'mo', 'po', 'pristine', 'prj', 'py', 'py-tpl', 'python', 'rst', 'sample', 'sh', 'shp', 'shx', 'svg', 'thtml', 'tpl', 'ttf', 'txt', 'TXT', 'unkn', 'unknown', 'vrt', 'woff', 'woff2', 'x', 'xml', 'yml'], 
        'FFmpeg': ['Makefile', 'S', 'asm', 'awk', 'bisect-create', 'c', 'cl', 'cl2c', 'clean-diff', 'makedef', 'mslink', 'configure', 'cpp', 'css', 'cu', 'cuh', 'dpx', 'dvd2concat', 'example', 'ffconcat', 'ffmeta', 'ffpreset', 'Makefile', 'fits', 'gen-rc', 'h', 'html', 'idx', 'init', 'libav-merge-next-commit', 'list', 'm', 'mailmap', 'mak', 'make_chlayout_test', 'md', 'missing_codec_desc', 'murge', 'pam', 'patcheck', 'pl', 'plotframes', 'pm', 'png', 'pnm', 'py', 'rb', 'rc', 'sample', 'sh', 'supp', 'template', 'texi', 'txt', 'unwrap-diff', 'v', 'voc', 'xsd', 'xwd', 'yml'], 
        'httpd': ['makefile', 'Makefile', '.awk', '.buildconf', '.c', '.cmake', '.cocci', '.conf', '.css', '.d', '.def', '.dsp', '.dtd', '.h', '.in', '.inc', '.js', '.ksh', '.ldap', '.lua', '.m4', '.manifest', '.mk', '.perl', '.pl', '.pro', '.properties', '.ps', '.py', '.rc', '.sh', '.tr', '.vbs', '.win', '.xml', '.xsl', '.y', '.yml'], 
        'struts': ['.cfg', '.cmd', '.css', '.dtd', '.eot', '.ftl', '.gdsl', '.html', '.idx', '.java', 'Jenkinsfile', '.jjt', '.jrxml', '.js', '.jsp', '.map', '.md', '.mvnw', '.pack', '.properties', '.sample', '.svg', '.tld', '.ttf', '.txt', '.vm', '.woff', '.woff2', '.xml', '.xsl', '.yaml', '.yml'], 
        'systemd': ['.h', '.c', '.sh', 'Makefile', 'SKELETON', '.arch', '.automount', '.awk', '.build', '.c', '.catalog', '.clang-format', '.cocci', '.conf', '.configure', '.css', '.ctags', '.dict', '.disabled', '.el', '.example', '.expected-err', '.expected-group', '.expected-passwd', '.fc', '.gperf', '.h', '.hwdb'], 
        'linux': ['Rakefile', '.a', '.aac', '.abc', '.ac', '.ac3', '.adm', '.adts', '.aff', '.ai', '.aidl', '.aif', '.aiff', '.am', '.amd64', '.amr', '.ani', '.antlr', '.apk', '.app', '.args', '.arj', '.arm', '.arm64', '.asciipb', '.asf', '.asis', '.asm', '.attr', '.avi', '.awk', '.babelrc', '.bat', '.bazel', '.bc', '.bcb', '.bdic', '.beg', '.begin', '.bgra', '.bin', '.BIN', '.bmp', '.bowerrc', '.br', '.bsdiff', 'BUILD', '.bz2', '.bzl', '.c', '.cab', '.cbor', '.cc', '.cer', '.cfg', '.cgi', '.clang-tidy', '.class', '.classes', '.classpath', '.cmake', '.cmd', '.cmx', '.cnf', '.code2flow', '.coffee', '.conf', '.config', '.content', '.context', '.cp', '.cpio', '.cpp', '.crashpad', '.crl', '.croc', '.cron', '.crossfile', '.crt', '.crx', '.crx2', '.crx3', '.cs', '.csproj', '.csr', '.css', '.css_t', '.csv', '.cti', '.cur', '.cxx', '.dart', '.dat', '.data', '.db', '.deb', '.def', '.defs', '.der', '.dex', '.dic', '.dict', '.diff', '.dirs', '.disable', '.dislocator', '.dj', '.dll', '.dm', '.dmg', '.doc', '.dot', '.dox', '.doxy', '.draft', '.dsc', '.dsp', '.dsw', '.dtd', '.dummy', '.dump', '.eac3', '.ejs', '.el', '.elm', '.ember-cli', '.emf', '.empty', '.end', '.ent', '.eot', '.eps', '.es', '.excludes', '.exe', '.expected', '.explain', '.export', '.exports', '.ext', '.extjs', '.fake', '.fallback', '.fbs', '.fea', '.fidl', '.filter', '.filters', '.first', '.flac', '.flags', '.flv', '.foo', '.fragment', '.g', '.gdb', '.gemspec', '.glif', '.gn', '.gni', '.go', '.golden', '.good', '.gpd', '.gperf', '.gpg', '.gradle', '.grd', '.grdp', '.groovy', '.gtestjs', '.guess', '.gyp', '.gypi', '.gz', '.gzip', '.h', '.handlebars', '.hashes', '.hbs', '.header', '.headers', '.hevc', '.hidden', '.hlsl', '.hml', '.lnk', '.log', '.lrz', '.lst', '.lz', '.lzma', '.lzo', '.m', '.m2ts', '.m32', '.m3u8', '.m4', '.m4a', '.make', 'Makefiles', '.mako', '.man', '.manifest', '.manpages', '.map', '.mc', '.md', '.menu', '.mht', '.mhtml', '.mingw', '.mips', '.mips64el', '.mipsel', '.mjs', '.mk', '.mkv', '.mm', '.mojom', '.mojomsg', '.mon', '.morph', '.msc', '.msg', '.msvc', '.myspell', '.myt', '.n', '.natvis', '.nc', '.nexe', '.nib', '.ninja', '.nmake', '.nmf', '.not-css', '.not-html', '.notpy', '.npmignore', '.nsproxy', '.nuspec', '.odt', '.oga', '.ogg', '.ogv', '.old', '.onc', '.options', '.opus', '.order', '.orf', '.otf', '.out', '.output', '.pam', '.patch', '.pb', '.pb_text', '.pch', '.pcm', '.pddm', '.pdf', '.pdl', '.pem', '.pfx', '.pgm', '.php', '.pidl', '.pins', '.pk8', '.pkg', '.pkgproj', '.pkpass', '.pl', '.plist', '.pltsuite', '.podspec', '.pol', '.polymer', '.Processor', '.proctype', '.prop', '.properties', '.props', '.proto', '.ps1', '.pump', '.pvk', '.pwg', '.py', '.pyd', '.pydeps', '.pyl', '.py-str', '.qemu', '.rar', '.rb', '.rc', '.rdf', '.release', '.resx', '.rgs', '.rm', '.rpc', '.rules', '.ruleset', '.rz', '.s', '.S', '.sample', '.sb', '.scons', '.scss', '.sct', '.sctlist', '.sdef', '.security', '.sed', '.see_also', '.settings', '.sh', '.sitx', '.skeletons', '.sln', '.snk', '.so', '.spc', '.spec', '.sql', '.sqlite', '.src', '.sst', '.status', '.storyboard', '.strings', '.sub', '.subtest', '.sug', '.swf', '.swift', '.sxg', '.sym', '.syms', '.syntax', '.tab', '.tar', '.tcl', '.templ', '.template', '.terms', '.test', '.testcases', '.test-mojom', '.tests', '.text', '.textpb', '.textproto', '.tlb', '.tmpl', '.tokencap', '.tokenizers', '.toml', '.ts', '.ttc', '.ttx', '.txt', '.TXT', '.typemap', '.types', '.unitjs', '.unix', '.usdz', '.vanilla', '.ver', '.version', '.visualizer', '.vpython', '.vsct', '.vsix', '.vtt', '.vue', '.wasm', '.wat', '.wbn', '.webarchive', '.whitelist', '.woff', '.woff2', '.wrong', '.wxs', '.xaml', '.xcf', '.xht', '.xhtml', '.xib', '.xls', '.xmb', '.xml', '.xpm', '.xsd', '.xsl', '.xslt', '.xtb', '.xul', '.xz', '.y', '.yaml', '.yapf', '.yml', '.yuv', '.Z', '.zoneinfo', '.zoo', '.zOS', '.ztf', '.zuc', '.zzz'],
        'chromium': ['Rakefile', '.a', '.aac', '.abc', '.ac', '.ac3', '.adm', '.adts', '.aff', '.ai', '.aidl', '.aif', '.aiff', '.am', '.amd64', '.amr', '.ani', '.antlr', '.apk', '.app', '.args', '.arj', '.arm', '.arm64', '.asciipb', '.asf', '.asis', '.asm', '.attr', '.avi', '.awk', '.babelrc', '.bat', '.bazel', '.bc', '.bcb', '.bdic', '.beg', '.begin', '.bgra', '.bin', '.BIN', '.bmp', '.bowerrc', '.br', '.bsdiff', 'BUILD', '.bz2', '.bzl', '.c', '.cab', '.cbor', '.cc', '.cer', '.cfg', '.cgi', '.clang-tidy', '.class', '.classes', '.classpath', '.cmake', '.cmd', '.cmx', '.cnf', '.code2flow', '.coffee', '.conf', '.config', '.content', '.context', '.cp', '.cpio', '.cpp', '.crashpad', '.crl', '.croc', '.cron', '.crossfile', '.crt', '.crx', '.crx2', '.crx3', '.cs', '.csproj', '.csr', '.css', '.css_t', '.csv', '.cti', '.cur', '.cxx', '.dart', '.dat', '.data', '.db', '.deb', '.def', '.defs', '.der', '.dex', '.dic', '.dict', '.diff', '.dirs', '.disable', '.dislocator', '.dj', '.dll', '.dm', '.dmg', '.doc', '.dot', '.dox', '.doxy', '.draft', '.dsc', '.dsp', '.dsw', '.dtd', '.dummy', '.dump', '.eac3', '.ejs', '.el', '.elm', '.ember-cli', '.emf', '.empty', '.end', '.ent', '.eot', '.eps', '.es', '.excludes', '.exe', '.expected', '.explain', '.export', '.exports', '.ext', '.extjs', '.fake', '.fallback', '.fbs', '.fea', '.fidl', '.filter', '.filters', '.first', '.flac', '.flags', '.flv', '.foo', '.fragment', '.g', '.gdb', '.gemspec', '.glif', '.gn', '.gni', '.go', '.golden', '.good', '.gpd', '.gperf', '.gpg', '.gradle', '.grd', '.grdp', '.groovy', '.gtestjs', '.guess', '.gyp', '.gypi', '.gz', '.gzip', '.h', '.handlebars', '.hashes', '.hbs', '.header', '.headers', '.hevc', '.hidden', '.hlsl', '.hml', '.lnk', '.log', '.lrz', '.lst', '.lz', '.lzma', '.lzo', '.m', '.m2ts', '.m32', '.m3u8', '.m4', '.m4a', '.make', 'Makefiles', '.mako', '.man', '.manifest', '.manpages', '.map', '.mc', '.md', '.menu', '.mht', '.mhtml', '.mingw', '.mips', '.mips64el', '.mipsel', '.mjs', '.mk', '.mkv', '.mm', '.mojom', '.mojomsg', '.mon', '.morph', '.msc', '.msg', '.msvc', '.myspell', '.myt', '.n', '.natvis', '.nc', '.nexe', '.nib', '.ninja', '.nmake', '.nmf', '.not-css', '.not-html', '.notpy', '.npmignore', '.nsproxy', '.nuspec', '.odt', '.oga', '.ogg', '.ogv', '.old', '.onc', '.options', '.opus', '.order', '.orf', '.otf', '.out', '.output', '.pam', '.patch', '.pb', '.pb_text', '.pch', '.pcm', '.pddm', '.pdf', '.pdl', '.pem', '.pfx', '.pgm', '.php', '.pidl', '.pins', '.pk8', '.pkg', '.pkgproj', '.pkpass', '.pl', '.plist', '.pltsuite', '.podspec', '.pol', '.polymer', '.Processor', '.proctype', '.prop', '.properties', '.props', '.proto', '.ps1', '.pump', '.pvk', '.pwg', '.py', '.pyd', '.pydeps', '.pyl', '.py-str', '.qemu', '.rar', '.rb', '.rc', '.rdf', '.release', '.resx', '.rgs', '.rm', '.rpc', '.rules', '.ruleset', '.rz', '.s', '.S', '.sample', '.sb', '.scons', '.scss', '.sct', '.sctlist', '.sdef', '.security', '.sed', '.see_also', '.settings', '.sh', '.sitx', '.skeletons', '.sln', '.snk', '.so', '.spc', '.spec', '.sql', '.sqlite', '.src', '.sst', '.status', '.storyboard', '.strings', '.sub', '.subtest', '.sug', '.swf', '.swift', '.sxg', '.sym', '.syms', '.syntax', '.tab', '.tar', '.tcl', '.templ', '.template', '.terms', '.test', '.testcases', '.test-mojom', '.tests', '.text', '.textpb', '.textproto', '.tlb', '.tmpl', '.tokencap', '.tokenizers', '.toml', '.ts', '.ttc', '.ttx', '.txt', '.TXT', '.typemap', '.types', '.unitjs', '.unix', '.usdz', '.vanilla', '.ver', '.version', '.visualizer', '.vpython', '.vsct', '.vsix', '.vtt', '.vue', '.wasm', '.wat', '.wbn', '.webarchive', '.whitelist', '.woff', '.woff2', '.wrong', '.wxs', '.xaml', '.xcf', '.xht', '.xhtml', '.xib', '.xls', '.xmb', '.xml', '.xpm', '.xsd', '.xsl', '.xslt', '.xtb', '.xul', '.xz', '.y', '.yaml', '.yapf', '.yml', '.yuv', '.Z', '.zoneinfo', '.zoo', '.zOS', '.ztf', '.zuc', '.zzz']
        }

# Short list of specific extensions to report data on
short = {'tomcat': ['.java'], 
        'django': ['.py'], 
        'FFmpeg': ['.c', '.cpp', '.cc', '.h'], 
        'httpd': ['.c', '.cpp', '.cc', '.h'], 
        'struts': ['.java', '.js'], 
        'systemd': ['.c', '.cpp', '.cc', '.h'],
        'linux': ['.c', '.cpp', '.cc', '.h'],
        'chromium': ['.c', '.cpp', '.cc', '.h']
        }

# The path to where the data to analyze is stored
DATA_PATH = "Data"

def sonar_read(files, data, project):
    """
    Reads the data returned by the SonarQube API
        Parameters:
            files (list): List of the files to check for metrix++ results
            data (dict): Dictionary mapping project name strings to lists of data
            proejct (string):  The current project to operate on
    """
    for file in files:
        if "sonar" in file:
            with open(DATA_PATH + "/" + file) as f:
                string_rep = f.read()
                replaced = string_rep.replace("\'singlequote2", "singlequote2") # Special case for this file that breaks the json parsing
                replaced = replaced.replace("\'", "\"")
                processed = json.loads(replaced)
                for entry in processed:
                    if float(entry['measures'][1]['value']) > 0:
                        data[project][entry['name']] = float(entry['measures'][0]['value'])/float(entry['measures'][1]['value'])


def metrix_read(files, data, project):
    """
    Reads the data created metrix++
        Parameters:
            files (list): List of the files to check for metrix++ results
            data (dict): Dictionary mapping project name strings to lists of data
            proejct (string):  The current project to operate on
    """
    temp_complexity = {}
    temp_lines = {}
    for file in files:
        if "metrixpp" in file:
            with open(DATA_PATH + "/" + file) as f:
                current_file = None
                complexity = None
                for line in f:
                    if "Overall metrics for 'std.code.complexity" in line:
                        current_file = line.split("::")[0]
                    if current_file is not None:
                        if "Total" in line:
                            if len(line.strip().split(":")) == 2:
                                complexity = float(line.strip().split(":")[1].strip())
                                # data[project][current_file] = complexity
                                temp_complexity[current_file] = complexity
                                current_file = None
                                complexity = None
            with open(DATA_PATH + "/" + file) as f:
                current_file = None
                lines = None
                for line in f:
                    if "Overall metrics for 'std.code.lines" in line:
                        current_file = line.split("::")[0]
                    if current_file is not None:
                        if "Total" in line:
                            if len(line.strip().split(":")) == 2:
                                lines = float(line.strip().split(":")[1].strip())
                                # data[project][current_file] = complexity
                                temp_lines[current_file] = lines
                                current_file = None
                                lines = None
    for key in temp_lines:
        if temp_lines[key] > 0:
            data[project][key] = temp_complexity[key]/temp_lines[key]


def main():
    """
    The main function, performs all data analysis and prints to the console 
    """
    file_dir = dict()
    data = dict()
    files = os.listdir(DATA_PATH)
    # Divide up by project
    for project in repos:
        file_dir[project] = list()
        for file in files:
            if project.lower() in file.lower():
                file_dir[project].append(file)
    # print(file_dir)
                


    for project in repos:
        data[project] = dict()
        sonar_read(file_dir[project], data, project)
        metrix_read(file_dir[project], data, project)

    # Write to a file
    with open("combined_complexity.json", "w") as f:
        f.write(json.dumps(data))

    # Calculate Stats for each
    for project in repos:
        print("Project (Tests Included):", project)
        # Total Complexity
        sum_u = []
        sum_n = []
        sum_t = []
        count_u = 0
        count_n = 0
        count_t = 0
        for entry in data[project]:
            flag = False
            # Check that entry's name ends with a valid extension
            for ending in repos[project]:
                if entry.endswith(ending):
                    flag=True
                    break
            if not flag:
                continue
            # Add to right place
            if 'util' in entry.lower() or 'helper' in entry.lower():
                sum_u.append(data[project][entry])
                sum_t.append(data[project][entry])
                count_u += 1
                count_t += 1
            else:
                sum_n.append(data[project][entry])
                sum_t.append(data[project][entry])
                count_n += 1
                count_t += 1

        print("Total:", count_t)
        # print("Total Complexity:", sum_t)
        print("Total Util:", count_u)
        # print("Total Util Complexity:", sum_u)
        print("Total Non-Util:", count_n)
        #print("Total Non-Util Complexity:", sum_n)
        if len(sum_t) != 0:
            print("Median:", statistics.median(sum_t))
            print("Mean:", statistics.mean(sum_t))
        if len(sum_u) != 0:
            print("Median Util:", statistics.median(sum_u))
            print("Mean Util:", statistics.mean(sum_u))
        if len(sum_n) != 0:    
            print("Median Non-util:", statistics.median(sum_n))
            print("Mean Non-util:", statistics.mean(sum_n))
        if len(sum_n) != 0 and len(sum_u) != 0:
            print("MWW: ", scipy.stats.mannwhitneyu(sum_u, sum_n))
        print("\n")
        print("Project (Tests Excluded):", project)
        
        # Total Complexity
        sum_u = []
        sum_n = []
        sum_t = []
        count_u = 0
        count_n = 0
        count_t = 0
        for entry in data[project]:
            if "test" in entry.lower():
                continue
            flag = False
            # Check that entry's name ends with a valid extension
            for ending in repos[project]:
                if entry.endswith(ending):
                    flag=True
                    break
            if not flag:
                continue
            # Add to right place
            if 'util' in entry.lower() or 'helper' in entry.lower():
                sum_u.append(data[project][entry])
                sum_t.append(data[project][entry])
                count_u += 1
                count_t += 1
            else:
                sum_n.append(data[project][entry])
                sum_t.append(data[project][entry])
                count_n += 1
                count_t += 1

        print("Total:", count_t)
        print("Total Util:", count_u)
        print("Total Non-Util:", count_n)
        if len(sum_t) != 0:
            print("Median:", statistics.median(sum_t))
            print("Mean:", statistics.mean(sum_t))
        if len(sum_u) != 0:
            print("Median Util:", statistics.median(sum_u))
            print("Mean Util:", statistics.mean(sum_u))
        if len(sum_n) != 0:    
            print("Median Non-util:", statistics.median(sum_n))
            print("Mean Non-util:", statistics.mean(sum_n))
        if len(sum_n) != 0 and len(sum_u) != 0:
            print("MWW: ", scipy.stats.mannwhitneyu(sum_u, sum_n))
        print("\n")

        # By Core Language
        for language in short[project]:
            sum_u = []
            sum_n = []
            sum_t = []
            count_u = 0
            count_n = 0
            count_t = 0
            for entry in data[project]:
                flag = False
                if entry.endswith(language) and ('util' in entry.lower() or 'helper' in entry.lower()):
                    sum_u.append(data[project][entry])
                    sum_t.append(data[project][entry])
                    count_u += 1
                    count_t += 1
                elif entry.endswith(language):
                    sum_n.append(data[project][entry])
                    sum_t.append(data[project][entry])
                    count_n += 1
                    count_t += 1
                else:
                    continue
            print("\n")
            print("Language (Tests Included):", language)
            print("Total:", count_t)
            print("Total Util:", count_u)
            print("Total Non-Util:", count_n)
            try:
                print("Median:", statistics.median(sum_t))
            except:
                print("Median: Divide by 0 error")
            try:
                print("Median Util:", statistics.median(sum_u))
            except:
                print("Median Util: Divide by 0 error")
            try:
                print("Median Non-util:", statistics.median(sum_n))
            except:
                print("Median Non-Util: Divide by 0 error")
            try:
                print("Mean:", statistics.mean(sum_t))
            except:
                print("Mean: Error")
            try:
                print("Mean Util:", statistics.mean(sum_u))
            except:
                print("Mean Util: Error")
            try:
                print("Mean Non-Util:", statistics.mean(sum_n))
            except:
                print("Mean Non-Util: Error")
            try:
                print("MWW: ", scipy.stats.mannwhitneyu(sum_u, sum_n))
            except:
                print("MWW Error")


            print("\n")

            sum_u = []
            sum_n = []
            sum_t = []
            count_u = 0
            count_n = 0
            count_t = 0
            for entry in data[project]:
                if "test" in entry.lower():
                    continue
                # Add to right place
                if entry.endswith(language) and ('util' in entry.lower() or 'helper' in entry.lower()):
                    sum_u.append(data[project][entry])
                    sum_t.append(data[project][entry])
                    count_u += 1
                    count_t += 1
                elif entry.endswith(language):
                    sum_n.append(data[project][entry])
                    sum_t.append(data[project][entry])
                    count_n += 1
                    count_t += 1
                else:
                    continue

            print("Language (Tests Excluded):", language)
            print("Total:", count_t)
            print("Total Util:", count_u)
            print("Total Non-Util:", count_n)
            try:
                print("Median:", statistics.median(sum_t))
            except:
                print("Median: Divide by 0 error")
            try:
                print("Median Util:", statistics.median(sum_u))
            except:
                print("Median Util: Divide by 0 error")
            try:
                print("Median Non-util:", statistics.median(sum_n))
            except:
                print("Median Non-Util: Divide by 0 error")
            try:
                print("Mean:", statistics.mean(sum_t))
            except:
                print("Mean: Error")
            try:
                print("Mean Util:", statistics.mean(sum_u))
            except:
                print("Mean Util: Error")
            try:
                print("Mean Non-Util:", statistics.mean(sum_n))
            except:
                print("Mean Non-Util: Error")
            try:
                print("MWW: ", scipy.stats.mannwhitneyu(sum_u, sum_n))
            except:
                print("MWW Error")

        # By C Group
        if ".c" not in short[project]:
            print("\n---------------------------------------------\n\n")
            continue

        sum_u = []
        sum_n = []
        sum_t = []
        count_u = 0
        count_n = 0
        count_t = 0
        for language in ['.c', '.cpp', '.cc', '.h']:

            for entry in data[project]:
                flag = False
                if entry.endswith(language) and ('util' in entry.lower() or 'helper' in entry.lower()):
                    sum_u.append(data[project][entry])
                    sum_t.append(data[project][entry])
                    count_u += 1
                    count_t += 1
                elif entry.endswith(language):
                    sum_n.append(data[project][entry])
                    sum_t.append(data[project][entry])
                    count_n += 1
                    count_t += 1
                else:
                    continue
        print("\n")
        print("Language (Tests Included): C Group")
        print("Total:", count_t)
        print("Total Util:", count_u)
        print("Total Non-Util:", count_n)
        try:
            print("Median:", statistics.median(sum_t))
        except:
            print("Median: Divide by 0 error")
        try:
            print("Median Util:", statistics.median(sum_u))
        except:
            print("Median Util: Divide by 0 error")
        try:
            print("Median Non-util:", statistics.median(sum_n))
        except:
            print("Median Non-Util: Divide by 0 error")
        try:
            print("Mean:", statistics.mean(sum_t))
        except:
            print("Mean: Error")
        try:
            print("Mean Util:", statistics.mean(sum_u))
        except:
            print("Mean Util: Error")
        try:
            print("Mean Non-Util:", statistics.mean(sum_n))
        except:
            print("Mean Non-Util: Error")
        try:
            print("MWW: ", scipy.stats.mannwhitneyu(sum_u, sum_n))
        except:
            print("MWW Error")

        print("\n")

        sum_u = []
        sum_n = []
        sum_t = []
        count_u = 0
        count_n = 0
        count_t = 0

        for language in ['.c', '.cpp', '.cc', '.h']:
            
            for entry in data[project]:
                if "test" in entry.lower():
                    continue
                # Add to right place
                if entry.endswith(language) and ('util' in entry.lower() or 'helper' in entry.lower()):
                    sum_u.append(data[project][entry])
                    sum_t.append(data[project][entry])
                    count_u += 1
                    count_t += 1
                elif entry.endswith(language):
                    sum_n.append(data[project][entry])
                    sum_t.append(data[project][entry])
                    count_n += 1
                    count_t += 1
                else:
                    continue

        print("Language (Tests Excluded): C Group")
        print("Total:", count_t)
        print("Total Util:", count_u)
        print("Total Non-Util:", count_n)
        try:
            print("Median:", statistics.median(sum_t))
        except:
            print("Median: Divide by 0 error")
        try:
            print("Median Util:", statistics.median(sum_u))
        except:
            print("Median Util: Divide by 0 error")
        try:
            print("Median Non-util:", statistics.median(sum_n))
        except:
            print("Median Non-Util: Divide by 0 error")
        try:
            print("Mean:", statistics.mean(sum_t))
        except:
            print("Mean: Error")
        try:
            print("Mean Util:", statistics.mean(sum_u))
        except:
            print("Mean Util: Error")
        try:
            print("Mean Non-Util:", statistics.mean(sum_n))
        except:
            print("Mean Non-Util: Error")
        try:
            print("MWW: ", scipy.stats.mannwhitneyu(sum_u, sum_n))
        except:
            print("MWW Error")


        print("\n---------------------------------------------\n\n")


if __name__ == '__main__':
    main()
