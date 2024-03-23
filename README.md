# ReadMe

### Directory Organization
- src: The code used for data collection and analysis
- complexity_data: The complexity measurements collected from SonarQube and Metrix++
- file_data: snapshot lists of the files from all used repositories along with the results of the odds ratios scripts.
- output_data: all the final data produced by the scripts specified below.

### Files to Remove for Metrix++
- Metrix++ fails entirely on what it considers to be malformed data. The following files were removed from the repositories for the Metrix++ process.
- From httpd
  - ./modules/aaa/mod_auth_digest.c
  - ./modules/metadata/mod_version.c

### SonarQube
- The code as provided assumes that SonarQube is being hosted locally with credentials configured as username: admin and password: password with the project called "test".
- The project token must be configured for proper transfer of data from Sonar Scanner to SonarQube.

### Intended Flow
- Clone each repostory to analyze
- Run vhp_cwes.py, vhp_vulns.py, and vhpdata.py to generate pre-requisite files
- Run odds_ratios.py and odds_ratios_no_renames.py. custom.py can be ran in place to specify the repository to run instead of running the collection in bulk.
- Run complexity_manager.py
- Run complexity_data.p
- Run clustering.py
- Run calls.py
- Run severity.py
- Run cwe_analysis.py
