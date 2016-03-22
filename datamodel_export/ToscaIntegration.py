import cloudshell.api.cloudshell_api as api
import re
import yaml


class ExportCloudShellTypes:
    def export(self, cloudshell_server, user, password, domain):
        session = api.CloudShellAPISession(cloudshell_server, user, password, domain)
        models = session.ExportFamiliesAndModels()
        """
            :type models: cloudshell.api.cloudshell_api.ExportConfigurationInfo
        """
        print models.Configuration
        import xml.etree.ElementTree as ET
        xmlstring = re.sub(' xmlns="[^"]+"', '', models.Configuration, count=1)
        tree = ET.fromstring(xmlstring)
        tosca = { 'tosca_definitions_version' : 'tosca_simple_yaml_1_0', 'description' : 'CloudShell node types' }
        node_types = {}

        node_types ['cloudshell.nodes.resource'] = {
                'derived_from' : 'root',
                'properties': { 'vendor' : {'type' : 'string'} }

            }

        for family in tree.findall("./ResourceFamilies/ResourceFamily"):
            if not family.get('IsService'):
                for model in family.findall("./Models/ResourceModel"):
                    name = 'cloudshell.nodes.{model_name}'.format(model_name=model.get('Name'))
                    node_types[name]= {
                        'derived_from' : 'cloudshell.nodes.resource'
                    }


        tosca ['node_types'] = node_types

        with open('result.yml', 'w') as yaml_file:
            yaml_file.write( yaml.dump(tosca, default_flow_style=False))


