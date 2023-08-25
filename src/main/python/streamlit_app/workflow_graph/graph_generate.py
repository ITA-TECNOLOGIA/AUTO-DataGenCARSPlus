import json

from graphviz import Digraph


class Workflow:

    def __init__(self, workflow_file_description):        
        self.workflow_file_description = workflow_file_description
        self.CARS_remove = ['C', 'CSc']

    def create_workflow(self, workflow_name, json_opt_params):
        """
        Creates a specific workflow.
        :param workflow_name: The workflow name.
        :param json_opt_params: A JSON with parameter values.
        :return: The generated workflow image path.
        """
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
                            if json_opt_params['init_step'] == 'True':
                                if node['condition'][0][0] == 'CARS':
                                    if json_opt_params['CARS'] == 'True':
                                        g.node(node['node_name'], color = 'red', shape='rect')
                                else:
                                    g.node(node['node_name'], color = 'red', shape='rect')
                            else:
                                draw_node = True                                
                                for condition in node['condition']:                                    
                                    if json_opt_params[condition[0]] != condition[1]:
                                        draw_node = False
                                        break
                                if draw_node:
                                    g.node(node['node_name'], shape='rect')

                        else:
                            g.node(node['node_name'], shape='rect')

                if 'gateways' in workflow.keys():
                    gateways = workflow['gateways']
                    for gateway in gateways:
                        if gateway['optional'] == 'False':
                            g.node(gateway['name'], shape='diamond', label=gateway['type'])
                        else:
                            draw_gateway = True
                            for condition in gateway['condition']:
                                if json_opt_params[condition[0]] != condition[1]:
                                    draw_gateway = False
                                    break
                            if draw_gateway:
                                g.node(gateway['name'], shape='diamond', label=gateway['type'])
                            
  
                # Add an edge connecting the two nodes
                arrows = workflow['arrows']
                for arrow in arrows:
                    if arrow['optional'] == 'False':
                        draw_arrow = True
                    else:
                        draw_arrow = True
                        for condition in arrow['condition']:
                            if json_opt_params[condition[0]] != condition[1]:
                                draw_arrow = False
                                break
                    if draw_arrow:
                        label = (arrow['label'][1:-1].split(','))
                        if 'CARS' in json_opt_params.keys() and json_opt_params['CARS'] == 'False':
                            for elem in self.CARS_remove:
                                if elem in label:
                                    label.remove(elem)
                        label_str = str(label)
                        if label_str.replace('[','').replace(']','').replace('\'','') == 'F' and json_opt_params['init_step'] == 'False':
                            label_str = '['+json_opt_params['file']+']'
                        g.edge(arrow['init_node'], arrow['end_node'], label=label_str.replace('\'',''))


                # add a legend to the graph
                with g.subgraph(name='legend') as legend:
                    legend.attr('node', shape='plaintext')
                    legend_text = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                                                <TR><TD PORT="files" COLSPAN="2">Files</TD></TR>'''
                    for legend_item in workflow['legend']:
                        quit = False
                        legend_item_text = data["legend"][legend_item]
                        if 'CARS' in json_opt_params.keys() and json_opt_params['CARS'] == 'False' and legend_item in self.CARS_remove:
                            pass
                        else:
                            if legend_item == 'F':
                                if  json_opt_params['init_step'] == 'False':
                                    legend_item = json_opt_params['file']
                                    legend_item_text = data["legend"][legend_item]
                                    quit = True
                                else: 
                                    if json_opt_params['CARS'] == 'False' and json_opt_params['init_step'] == 'True':
                                        legend_item_text = 'File from U, I'
                            legend_text = legend_text + '''<TR><TD ALIGN="LEFT">'''+legend_item+'''</TD><TD ALIGN="LEFT">'''+legend_item_text+'''</TD></TR>'''
                        if quit:
                            break
                    legend_text = legend_text + '''</TABLE>>'''
                    legend.node('legend', legend_text)

                # Save the graph as a PNG file
                path = g.render(filename='src/main/python/streamlit_app/workflow/'+workflow['workflow_name'], format='png', cleanup=True)
                return path        
        return 'Workflow not found'


if __name__ == "__main__":
    wf = Workflow()
    json_opt_params = {}
    json_opt_params['CARS'] = 'True'
    json_opt_params['NULLValues'] = 'True'
    json_opt_params['init_step'] = 'True'
    path = wf.create_workflow('ReplicateDataset', json_opt_params)