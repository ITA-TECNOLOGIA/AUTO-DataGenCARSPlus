from graphviz import Digraph
import json


class Workflow:

    def __init__(self):
        self.workflow_file_description = 'src/main/python/streamlit_app/workflow/workflows.json'

    def create_workflow(self, workflow_name, json_opt_params):
        with open(self.workflow_file_description, 'r') as f:
            # Load the JSON data into a Python dictionary
            data = json.load(f)

        for workflow in data['workflows']:
            if workflow['workflow_name'] == workflow_name:
                # Create a directed graph object
                g = Digraph()#, format='png')

                # Add two nodes to the graph
                nodes = workflow['nodes']
                for node in nodes:
                    if node['node_name'] == 'BEGIN' or node['node_name'] == 'END':
                        g.node(node['node_name'], shape='circle')
                    else:
                        if node['optional'] == 'True':
                            g.node(node['node_name'], color = 'red', shape='rect')
                        else:
                            g.node(node['node_name'], shape='rect')

                if 'gateways' in workflow.keys():
                    gateways = workflow['gateways']
                    for gateway in gateways:
                        if gateway['type'] == 'exclusive':
                            g.node(gateway['name'], shape='diamond', label='X')
                        elif gateway['type'] == 'parallel':
                            g.node(gateway['name'], shape='diamond', label='+')

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
                        legend_text = legend_text + '''<TR><TD ALIGN="LEFT">'''+legend_item+'''</TD><TD ALIGN="LEFT">'''+data["legend"][legend_item]+'''</TD></TR>'''
                    legend_text = legend_text + '''</TABLE>>'''
                    legend.node('legend', legend_text)

                # Save the graph as a PNG file
                path = g.render(filename='src/main/python/streamlit_app/workflow/'+workflow['workflow_name'], format='png', cleanup=True)
                
                return path
        
        return 'Workflow not found'

if __name__ == "__main__":
    wf = Workflow()
    print(wf.create_workflow('MappingToCategorization', 0))