#!/usr/bin/env python3
# coding: utf-8

""" Vim Plugin to manipulate systemVerilog sources """

import vim


def get_module_info(verilog):
    """ Return a dict containing all the
    module information """

    into_comment = "No"
    module_found = "No"
    parameter_found = "No"
    io_found = "No"

    instance = {"name": "", "io": [], "parameter": []}

    for line in verilog:

        line = line.strip()

        # Detect comment block and avoid to parse them
        if line[0:1] == "/*":
            into_comment = "Yes"

        elif line[0:1] == "*/" or line[-2:] == "*/":
            into_comment = "No"

        if into_comment == "Yes":
            continue

        # Search for the module name
        if module_found == "No":

            if "module" in line:

                module_found = "Yes"
                info = line.split(" ")
                instance["name"] = info[1]

                if instance["name"][-1] == ";":
                    instance["name"] = instance["name"][:-1]

        # Search for the parameter if present
        if parameter_found == "No":

            if line[0:9] == "parameter":

                _line = line.split("//")[0].strip()
                _line = _line.replace("\t", " ")
                _line = _line.replace(",", ";")

                if _line[-1] != ";":
                    _line = _line + ";"

                instance["parameter"].append(_line)

        # Search for the input and output
        if io_found == "No":

            if line[0:5] == "input":

                _line = line.split("//")[0].strip()
                _line = _line.replace("signed", "wire")
                _line = _line.replace("reg", "wire")
                _line = _line.replace(",", ";")
                _line = _line.replace("input", "")

                instance["io"].append(_line.strip())

            if line[0:6] == "output":

                _line = line.split("//")[0].strip()
                _line = _line.replace(",", ";")
                _line = _line.replace("signed", "wire")
                _line = _line.replace("output", "")

                if _line[-1] != ";":
                    _line = _line + ";"

                instance["io"].append(_line.strip())

    return instance


def create_instance(instance):
    """ Parse `instance` dictionnary and create the
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

            _param = param.split(" ")
            _name = _param[-3]

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
