from graphviz import Digraph
import json
import config as cf

class Workflow:

    def __init__(self):
        self.workflow_file_description = cf.WORKFLOWS_DESCRIPTION

    def create_workflow(self):
        with open(self.workflow_file_description, 'r') as f:
            # Load the JSON data into a Python dictionary
            data = json.load(f)

        for workflow in data['workflows']:
            # Create a directed graph object
            g = Digraph('G', filename=workflow['workflow_name'], format='png')

            # Add two nodes to the graph
            nodes = workflow['nodes']
            for node in nodes:
                if node['optional'] == 'True':
                    g.node(node['node_name'], color = 'red')
                else:
                    g.node(node['node_name'])
            

            # Add an edge connecting the two nodes
            arrows = workflow['arrows']
            for arrow in arrows:
                g.edge(arrow['init_node'], arrow['end_node'], label=arrow['label'])

            # add a legend to the graph
            with g.subgraph(name='legend') as legend:
                legend.attr('node', shape='plaintext')
                legend_text = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                                            <TR><TD PORT="files" COLSPAN="2">Files</TD></TR>'''
                for legend_item in workflow['legend']:
                    key = legend_item['short_name']
                    value = legend_item['description']
                    legend_text = legend_text + '''<TR><TD ALIGN="LEFT">'''+key+'''</TD><TD ALIGN="LEFT">'''+value+'''</TD></TR>'''
                legend_text = legend_text + '''</TABLE>>'''
                legend.node('legend', legend_text)

            # Save the graph as a PNG file
            g.render()
