import errno,os,subprocess,sys, shutil
from subprocess import CalledProcessError


# The following function extracts the tar gz files. It is taken from
# http://code.activestate.com/recipes/576714-extract-a-compressed-file/

def extract_file(path, to_directory='.'):
    import tarfile,zipfile
    path = os.path.expanduser(path)
    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'
    else:
        raise ValueError, "Could not extract `%s` as no appropriate extractor is found" % path

    cwd = os.getcwd()
    os.chdir(to_directory)

    try:
        file = opener(path, mode)
        try: file.extractall()
        finally: file.close()
    finally:
        os.chdir(cwd)

# Taken from
# http://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python

def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("on", "yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("off", "no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))

def writeOptions(root,config):
    """Write out options in a format suitable for a shell script"""

    fname=".options.cfg"
    full_path=root+"/"+fname
    f=open(full_path,'w')
    f.write("# This file is created automatically by bempp_setup.py\n")
    for section in config.sections():
        for option in config.items(section):
            f.write(section+"_"+option[0]+"="+"\""+option[1]+"\""+"\n")
    f.close()
    build_dir=config.get('Main','build_dir')
    shutil.copyfile(full_path,build_dir+"/"+fname)


def setDefaultConfigOption(config,section,option,value, overwrite=False):
    """Enter a default option into the ConfigParser object 'config'. If option already exists returns
       the existing value, otherwise the value 'value'.
    """

    if config.has_option(section,option) and not overwrite:
        return config.get(section,option)
    else:
        if not config.has_section(section): config.add_section(section)
        config.set(section,option,value)
        return value

def pythonInfo():
    """Return a tuple (exe,lib,include) with the paths of the Python Interpeter, Python library and include directory"""

    import sys,os

    exe = sys.executable
    lib_no_suffix = sys.prefix+"/lib/libpython"+str(sys.version_info[0])+"."+str(sys.version_info[1])
    if sys.platform.startswith('darwin'):
        lib = lib_no_suffix+".dylib"
    elif sys.platform.startswith('linux'):
        lib = lib_no_suffix+".so"
    else:
        raise Exception("Platform not supported")
    if not os.path.isfile(lib):
        lib = lib_no_suffix+".a"
        if not os.path.isfile(lib):
            raise Exception("Could not find Python library in "+sys.prefix+"/lib/")
    include = (sys.prefix+"/include/python"+
               str(sys.version_info[0])+"."+str(sys.version_info[1]))
    return (exe,lib,include)

def download(fname,url,dir):
    """Download a file from a url into the directory dir if the file does not already exist"""
    from py_modules.urlgrabber import urlgrab,progress
    if not os.path.isfile(dir+"/"+fname):
        urlgrab(url,filename=dir+"/"+fname,progress_obj=progress.TextMeter(),reget='simple')

def checkCreateDir(dir):
    """Create a directory if it does not yet exist"""
    if not os.path.isdir(dir):
        os.makedirs(os.path.abspath(dir))

def to_int(s,min_val=1):
    """Convert string s to integer. if int(s)<min_val return min_val"""
    i = int(s)
    if i>min_val:
        return i
    else:
        return min_val

def testBlas(root,config):
    """Test if BLAS functions correctly and set whether G77 calling convention is needed"""
    cwd = os.getcwd()
    blas = config.get('BLAS','lib')
    cxx=config.get('Main','cxx')
    cc=config.get('Main','cc')
    cflags = config.get('Main','cflags')
    cxxflags = config.get('Main','cxxflags')
    prefix = config.get('Main','prefix')
    cmake_exe = config.get('CMake','exe')
    fnull = open(os.devnull,'w')

    if sys.platform.startswith('darwin'):
        ld_path = "export DYLD_LIBRARY_PATH="+prefix+"/bempp/lib:$DYLD_LIBRARY_PATH; "
    elif sys.platform.startswith('linux'):
        ld_path = "export LD_LIBRARY_PATH="+prefix+"/bempp/lib:$LD_LIBRARY_PATH; "
    else:
        raise Exception("Wrong architecture.")


    os.mkdir(root+"/test_blas/build")
    os.chdir(root+"/test_blas/build")
    config_string = "CC="+cc+" CXX="+cxx+" CFLAGS='"+cflags+"' CXXFLAGS='"+cxxflags+"' "+cmake_exe+" -D BLAS_LIBRARIES:STRING=\""+blas+"\" .."
    try:
        subprocess.check_output(config_string,shell=True,stderr=subprocess.STDOUT)
        subprocess.check_output("make",stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, ex:
        fnull.close()
        raise Exception("Building BLAS tests failed with the following output:\n" +
                        ex.output +
                        "Please check your compiler and BLAS library settings.")
    try:
        subprocess.check_output(ld_path+"./test_blas",shell=True,
                                stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, ex:
        os.chdir(cwd)
        fnull.close()
        raise Exception("BLAS test failed with the following output:\n" +
                        ex.output +
                        "Please check your libraries and your DYLD_LIBRARY_PATH "
                        "or LD_LIBRARY_PATH settings.")

    # Test for zdotc convention
    g77 = False
    try:
        subprocess.check_call(ld_path+"./test_zdotc",shell=True,stdout=fnull,stderr=fnull)
    except:
        g77 = True
    if g77:
        try:
            subprocess.check_call(ld_path+"./test_zdotc_g77",shell=True,
            stdout=fnull,stderr=fnull)
        except:
            os.chdir(cwd)
            fnull.close()
            raise Exception("ZDOTC works neither in G77 nor in GFortran modus. "
                            "Please check your BLAS libraries")
        setDefaultConfigOption(config,'AHMED','with_g77','ON',overwrite=True)
    else:
        setDefaultConfigOption(config,'AHMED','with_g77','OFF',overwrite=True)
    os.chdir(cwd)
    print "BLAS configuration successfully completed."

def testLapack(root,config):
    """Test if BLAS functions correctly and set whether G77 calling convention is needed"""
    cwd = os.getcwd()
    blas = config.get('BLAS','lib')
    lapack = config.get('LAPACK','lib')
    cxx=config.get('Main','cxx')
    cc=config.get('Main','cc')
    cflags = config.get('Main','cflags')
    cxxflags = config.get('Main','cxxflags')
    cmake_exe = config.get('CMake','exe')
    prefix = config.get('Main','prefix')
    fnull = open(os.devnull,'w')

    if sys.platform.startswith('darwin'):
        ld_path = "export DYLD_LIBRARY_PATH="+prefix+"/bempp/lib:$DYLD_LIBRARY_PATH; "
    elif sys.platform.startswith('linux'):
        ld_path = "export LD_LIBRARY_PATH="+prefix+"/bempp/lib:$LD_LIBRARY_PATH; "
    else:
        raise Exception("Wrong architecture.")

    os.mkdir(root+"/test_lapack/build")
    os.chdir(root+"/test_lapack/build")
    config_string = "CC="+cc+" CXX="+cxx+" CFLAGS='"+cflags+"' CXXFLAGS='"+cxxflags+"' "+cmake_exe+" -D BLAS_LIBRARIES:STRING=\""+blas+"\" -D LAPACK_LIBRARIES=\""+lapack+"\" .."
    try:
        subprocess.check_output(config_string,shell=True,stderr=subprocess.STDOUT)
        subprocess.check_output("make",shell=True,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, ex:
        fnull.close()
        raise Exception("Building LAPACK tests failed with the following output:\n" +
                        ex.output +
                        "\nPlease check your compiler as well as BLAS and Lapack "
                        "library settings.\n")
    try:
        subprocess.check_output(ld_path+ "./test_lapack",shell=True,
                                stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, ex:
        os.chdir(cwd)
        fnull.close()
        raise Exception("LAPACK test failed with the following output:\n" +
                        ex.output +
                        "Please check your libraries and your DYLD_LIBRARY_PATH "
                        "or LD_LIBRARY_PATH settings.")
    os.chdir(cwd)
    fnull.close()
    print "LAPACK configuration successfully completed."

def checkDeleteDirectory(dir):
    """Delete directory dir if it exists"""
    if os.path.isdir(dir): shutil.rmtree(dir)

def checkDeleteFile(s):
    """Delete file given by path in string s if it does not exist"""
    if os.path.exists(s):
        os.remove(s)

def cleanUp(root,config):
    """Clean up so that a rerun of the installer is possible"""

    prefix=config.get('Main','prefix')
    checkDeleteDirectory(prefix+"/bempp")
    checkDeleteDirectory(root+"/test_blas/build")
    checkDeleteDirectory(root+"/test_lapack/build")

def setCompilerOptions(config,section):
    """Update the compiler Options in 'section' with those from 'Main'"""

    setDefaultConfigOption(config,section,'cc',config.get('Main','cc'))
    setDefaultConfigOption(config,section,'cxx',config.get('Main','cxx'))
    setDefaultConfigOption(config,section,'optflags',config.get('Main','optflags'))
    setDefaultConfigOption(config,section,'cflags',config.get('Main','cflags'))
    setDefaultConfigOption(config,section,'cxxflags',config.get('Main','cxxflags'))

    optflags = config.get(section,'optflags')
    cflags = config.get(section,'cflags')
    cxxflags = config.get(section,'cxxflags')

    config.set(section,'cflags',cflags + " " + optflags)
    config.set(section,'cxxflags',cxxflags + " " + optflags)