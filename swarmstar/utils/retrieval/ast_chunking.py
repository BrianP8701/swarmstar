import ast

def find_class_start_end_lines(file_path, class_name):
    """Find the start and end lines of a class in the given file."""
    
    # Read the source code from the file
    with open(file_path, 'r') as file:
        source_code = file.read()
            
    # Parse the source code into an AST
    tree = ast.parse(source_code)
    
    # Define a class visitor to find the specific class
    class ClassVisitor(ast.NodeVisitor):
        def __init__(self):
            self.start_line = None
            self.end_line = None

        def visit_ClassDef(self, node):
            """Visit a class definition."""
            if node.name == class_name:
                # Found the class, get its start line
                self.start_line = node.lineno
                # Python 3.8 and later: directly use end_lineno if available
                self.end_line = getattr(node, 'end_lineno', None)
                
                # For Python versions < 3.8, find the end line by looking at the last body element
                if self.end_line is None and node.body:
                    # The last element of the class body might not be the actual last line (e.g., comments),
                    # but it's a reasonable approximation without parsing comments.
                    self.end_line = node.body[-1].lineno
                
                # Stop visiting more nodes
                raise StopIteration

    # Create the visitor and visit the AST nodes
    visitor = ClassVisitor()
    try:
        visitor.visit(tree)
    except StopIteration:
        pass  # Expected behavior to stop after finding the class
    
    # Return the start and end lines
    return visitor.start_line, visitor.end_line
