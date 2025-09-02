
import argparse
import io
import os
import sys
from cli_formatter.output_formatting import warning, error, info, print_headline_banner
import json

from eml_analyzer.library.outputs import AbstractOutput, StandardOutput, JsonOutput
from eml_analyzer.library.parser import ParsedEmail, EmlParsingException, Attachment


def analyze(eml_filename,output_dir):
    file_name_secured=eml_filename # email à traiter
    
    print("default")
    #default file
    with open(file_name_secured, 'r', encoding='utf-8', errors="replace") as eml_file :
        default_output_format: AbstractOutput = StandardOutput() # output format
        default_eml_file = _read_eml_file_or_exit_on_error(output_format=default_output_format, input_file=eml_file)
        default_parsed_email: ParsedEmail = _parse_eml_file_or_exit_on_error(output_format=default_output_format, eml_content=default_eml_file)

    print("json")
    # Json file
    with open(file_name_secured, 'r', encoding='utf-8', errors="replace") as eml_file :
        json_output_format: AbstractOutput = JsonOutput() # output format
        json_eml_file = _read_eml_file_or_exit_on_error(output_format=json_output_format, input_file=eml_file)
        json_parsed_email: ParsedEmail = _parse_eml_file_or_exit_on_error(output_format=json_output_format, eml_content=json_eml_file)
        

    print("vars")
    #File
    parsed_email=json_parsed_email
    output_format=json_output_format
    eml_file=json_eml_file

    header = True
    structure = True
    url = True
    tracking = True
    
    text= True
    html= True

    extract_all=True

    output=output_dir

    if header:
        output_format.process_option_show_header(parsed_email=parsed_email)
    if structure:
        output_format.process_option_show_structure(parsed_email=parsed_email)
    if url:
        output_format.process_option_show_embedded_urls_in_html_and_text(parsed_email=parsed_email)
    if tracking:
        output_format.process_option_show_reloaded_content_from_html(parsed_email=parsed_email)
    if text:
        output_format.process_option_show_text(parsed_email=parsed_email)
    if html:
        output_format.process_option_show_html(parsed_email=parsed_email)

    print("extractall")
    if extract_all :
        _extract_all_attachments(parsed_email=default_parsed_email, path=output)
    print("getfinal")
    final_output = output_format.get_final_output(parsed_email=parsed_email)
    
    return final_output


def _read_eml_file_or_exit_on_error(output_format: AbstractOutput, input_file: io.TextIOWrapper) -> str:
    try:
        with input_file:
            return input_file.read()
    except Exception as e:
        print('File could not be loaded -> check the encoding of the file')
        output_format.output_error_and_exit(exception=e, error_message='File could not be loaded')


def _parse_eml_file_or_exit_on_error(output_format: AbstractOutput, eml_content: str) -> ParsedEmail:
    try:
        return ParsedEmail(eml_content=eml_content)
    except EmlParsingException as e:
        print('File could not be parsed. Sure it is an eml file?')
        output_format.output_error_and_exit(exception=e, error_message='File could not be parsed. Sure it is an eml file?')


def _write_attachment_to_file(attachment: Attachment, output_path) -> None:
    output_path = _get_output_path_for_attachment(attachment=attachment, output_path=output_path)

    output_file = open(output_path, mode='wb')
    output_file.write(attachment.content)
    info('Attachment [{}] "{}" extracted to {}'.format(attachment.index, attachment.filename, output_path))


def _get_output_path_for_attachment(attachment: Attachment, output_path) -> str:
    if output_path is None:
        return attachment.filename
    elif os.path.isdir(output_path):
        return os.path.join(output_path, attachment.filename)


def _extract_all_attachments(parsed_email: ParsedEmail, path):
    print_headline_banner('Extracting All Attachments')

    # if no output directory is given then a default directory with the name 'eml_attachments' is used
    if path is None:
        path = 'eml_attachments'

    if not os.path.exists(path):
        os.makedirs(path)

    for attachment in parsed_email.get_attachments():
        _write_attachment_to_file(attachment=attachment, output_path=path)


if __name__ == '__main__':
    email="../exemple/email3.eml"
    output="../exemple/outputdir"
    analyze(email,output)