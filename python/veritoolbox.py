#!/usr/bin/env python3
# coding: utf-8

""" Vim Plugin to manipulate systemVerilog sources """

import vim


def get_module_info(verilog):
    """ Return a dict containing all the
    module information """

    # List of flags activated during parsing steps.
    intoComment = "No"
    inlineComment = "Yes"
    moduleFound = "No"
    parameterFound = "No"
    ioFound = "No"

    instance = {"name": "", "io": [], "parameter": []}

    for line in verilog:

        # Remove space at beginning and end of line
        line = line.strip()

        # Detect comment block in header
        # and avoid to parse them
        if line[0:2] == "/*":
            intoComment = "Yes"
            inlineComment = "No"
        elif line[0:2] == "//":
            intoComment = "Yes"
            inlineComment = "Yes"
        elif line[0:2] == "*/" or line[-2:] == "*/":
            intoComment = "No"
            inlineComment = "No"

        if intoComment == "Yes":
            if inlineComment == "Yes":
                intoComment = "No"
            continue

        # Search for the module name
        # if `module` found, split line with " "
        # and get the last part, the name.
        # Expect `module module_name`alone on the line
        if moduleFound == "No":
            if "module" in line:
                moduleFound = "Yes"
                info = line.split(" ")
                instance["name"] = info[1]
                if instance["name"][-1] == ";":
                    instance["name"] = instance["name"][:-1]

        # Search for the parameter if present search a line with `parameter`,
        # remove comment at the end of line, replace comma with semicolon and
        # store the line, ready to be written as a parameter declaration in
        # testsuite file
        if parameterFound == "No":
            if line[0:9] == "parameter":
                _line = line.split("//")[0].strip()
                _line = _line.replace("\t", " ")
                _line = _line.replace(",", "")
                if _line[-1] != ";":
                    _line = _line + ";"
                instance["parameter"].append(_line)

        # Search for input or ouput, change comma to semicolon, signed|wire to
        # reg and remove IO mode. Remove comment at the end of line
        # Ready to be written into testsuitefile.
        if ioFound == "No":
            if line[0:5] == "input" or line[0:6] == "output":
                _line = line.split("//")[0].strip()
                if line[0:10] == "input var ":
                    _line = _line.replace("input var", "")
                else:
                    _line = _line.replace("input", "")
                _line = _line.replace("output", "")
                _line = _line.replace("signed", "logic")
                _line = _line.replace("wire", "logic")
                _line = _line.replace("reg", "logic")
                _line = _line.replace(",", "")
                _line = _line + ";"
                instance["io"].append(_line.strip())

    return instance


def create_instance(instance):
    """ Parse instance dictionary and create the
    instance to drop in the buffer """

    _text = "\n"

    # Print parameter declarationif present
    if instance["parameter"]:
        for param in instance["parameter"]:
            _text += """    """ + param + "\n"
        _text += """\n"""

    # Print input/output declaration if present
    if instance["io"]:
        for ios in instance["io"]:
            _text += """    """ + ios + "\n"
        _text += """\n"""

    # Write the instance
    _text += """    """ + instance["name"] + " \n"

    # Print parameter instance if present
    if instance["parameter"]:
        _text += """    #(\n"""

        # First get the longest name
        maxlen = 0
        for idx, param in enumerate(instance["parameter"]):

            _param = param.split(" ")
            _name = _param[-3]

            if len(_name) > maxlen:
                maxlen = len(_name)

        # Then pass to declare the param in the instance
        for idx, param in enumerate(instance["parameter"]):

            # get left and right side around the equal sign
            _param = param.split("=")
            # split over space of the let side ('parameter param_name')
            _param = _param[-2].split(" ")
            # remove empty element in the list
            _param = list(filter(None, _param))
            _name = _param[-1]

            _text += "    ." + _name + \
                " " * (maxlen - len(_name)) + \
                " (" + _name + ")"

            if idx == len(instance["parameter"]) - 1:
                _text += "\n"
            else:
                _text += ",\n"

        _text += "    )\n"

    _text += """    dut \n    (\n"""

    # Print input/output instance if present
    if instance["io"]:

        # First get the longest name
        maxlen = 0
        for idx, ios in enumerate(instance["io"]):
            _io = ios.split(" ")
            _name = _io[-1][:-1]
            if len(_name) > maxlen:
                maxlen = len(_name)

        # Then pass to declare the io in the instance
        for idx, ios in enumerate(instance["io"]):

            _io = ios.split(" ")
            _name = _io[-1][:-1]

            _text += "    ." + _name + \
                " " * (maxlen - len(_name)) + \
                " (" + _name + " " * (maxlen - len(_name)) + ")"

            if idx == len(instance["io"]) - 1:
                _text += "\n"
            else:
                _text += ",\n"

    _text += """    );\n"""

    return _text


def insert_sv_instance():
    """ Read the " buffer and extract a
    verilog instance, insert the instance
    on current line """

    # Get the " buffer content defined in upper vimscript
    buf = vim.eval("buf")
    buf = buf.split("\n")

    (row, _) = vim.current.window.cursor

    # Extract the module information
    info = get_module_info(buf)
    # Create the instance from previous information
    instance = create_instance(info)

    # Split new content on newline
    # Vim doesn't allow \n
    _inst = instance.split("\n")

    # Append new content under cursor row
    vim.current.buffer.append(_inst, row)
