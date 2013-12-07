from django import template

def get_att_list_var(tag_name, tag_args):
    att_list_var = tag_args.get('from')
    if not att_list_var:
        raise template.TemplateSyntaxError, "%r is missing 'from' parameter" % tag_name
    return att_list_var
    
def get_context_var(tag_name, tag_args):
    return tag_args.get('as')
    
def get_att_types(tag_name, tag_args):
    only_att_types = tag_args.get('only')
    not_att_types = tag_args.get('not')
    
    if only_att_types and not_att_types:
        raise template.TemplateSyntaxError, "%r cannot have both 'only' and 'not' parameters" % tag_name
        
    att_types_list = []
    
    att_types = only_att_types or not_att_types
    if att_types:
        att_types = parse_string(tag_name, att_types, 'attachment type')
        att_types_list = att_types.split(',')
    
    return att_types_list, bool(not_att_types)
    
def get_num(tag_name, tag_args):
    num = tag_args.get('limit')
    if num:
        num = parse_num(tag_name, num, 'limit')
    return num

def parse_string(tag_name, quoted_str, param):
    arg_str = ''
    
    try:
        if not (quoted_str[0] == quoted_str[-1] and quoted_str[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r has invalid '%s' parameter" % (tag_name, param)
        arg_str = quoted_str[1:-1]
    except IndexError:
        raise template.TemplateSyntaxError, "%r is missing '%s' parameter" % (tag_name, param)
        
    return arg_str

def parse_num(tag_name, num_str, param, positive=True):
    num = 0

    try:
        num = int(num_str)
        if positive and num < 1:
            raise ValueError
    except ValueError:
        raise template.TemplateSyntaxError, "%r has invalid '%s' argument" % (tag_name, param)
        
    return num
    
def parse_args(tag_name, bits, valid_params):
    tag_args = {}

    while bits:
        param = bits.pop()
        if not param in valid_params:
            raise template.TemplateSyntaxError, "%r has unexpected '%s' parameter" % (tag_name, param)
            
        try:
            tag_args[param] = bits.pop()
        except IndexError:
            raise template.TemplateSyntaxError, "%r is missing '%s' argument" % (tag_name, param)
                        
    return tag_args
