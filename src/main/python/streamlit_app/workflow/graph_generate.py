from graphviz import Digraph
import json


class Workflow:

    def __init__(self):
        self.workflow_file_description = 'src/main/python/streamlit_app/workflow/workflows.json'
        self.CARS_remove = ['C', 'CSc']

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
                            if json_opt_params['init_step'] == 'True':
                                g.node(node['node_name'], color = 'red', shape='rect')
                            else:
                                if json_opt_params[node['condition']] == 'True':
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
                    print(arrow)
                    if arrow['optional'] == 'False':
                        draw_arrow = True
                    else:
                        draw_arrow = True
                        for condition in arrow['condition']:
                            print(condition)
                            if json_opt_params[condition[0]] != condition[1]:
                                draw_arrow = False
                                break
                    if draw_arrow:
                        label = (arrow['label'][1:-1].split(','))
                        print(label)
                        if 'CARS' in json_opt_params.keys() and json_opt_params['CARS'] == 'False':
                            for elem in self.CARS_remove:
                                if elem in arrow['label']:
                                    label.remove(elem)
                        label_str = str(label)
                        g.edge(arrow['init_node'], arrow['end_node'], label=label_str.replace('\'',''))


                # add a legend to the graph
                with g.subgraph(name='legend') as legend:
                    legend.attr('node', shape='plaintext')
                    legend_text = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                                                <TR><TD PORT="files" COLSPAN="2">Files</TD></TR>'''
                    for legend_item in workflow['legend']:
                        if 'CARS' in json_opt_params.keys() and json_opt_params['CARS'] == 'False' and legend_item in self.CARS_remove:
                            pass
                        else:
                            legend_text = legend_text + '''<TR><TD ALIGN="LEFT">'''+legend_item+'''</TD><TD ALIGN="LEFT">'''+data["legend"][legend_item]+'''</TD></TR>'''
                    legend_text = legend_text + '''</TABLE>>'''
                    legend.node('legend', legend_text)

                # Save the graph as a PNG file
                path = g.render(filename='src/main/python/streamlit_app/workflow/'+workflow['workflow_name'], format='png', cleanup=True)
                
                return path
        
        return 'Workflow not found'

if __name__ == "__main__":
    wf = Workflow()
    json_opt_params = {}
    json_opt_params['CARS'] = "True"
    json_opt_params['NULLValues'] = "True"
    json_opt_params['init_step'] = "True"
    print(wf.create_workflow('ReplicateDataset', json_opt_params))