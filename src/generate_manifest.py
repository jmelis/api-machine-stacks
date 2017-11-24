#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml.etree import SubElement, Element, ElementTree, tostring


class PomXMLTemplate:

    def __init__(self, json_data):
        self._data = json_data
        self.root = Element(
            'project',
            xmlns="http://maven.apache.org/POM/4.0.0",
        )
        self.tree = ElementTree(self.root)
        self.create()

    def create(self):
        self._packages = self._data.get('packages')
        SubElement(self.root, 'modelVersion').text = '4.0.0'
        SubElement(self.root, 'packaging').text = 'pom'
        SubElement(self.root, 'url').text = 'https://example.com'
        self.licenses = SubElement(self.root, 'licenses')
        self.license = SubElement(self.licenses, 'license')
        SubElement(
            self.license, 'name').text = "Apache License, Version 2.0"
        SubElement(
            self.license, 'url').text = "http://www.apache.org/licenses"
        self.add_dependencies(self._packages)

    def add_dependencies(self, dependencies):
        if dependencies:
            self.dpmanage = SubElement(self.root, "dependencyManagement")
            self.dps = SubElement(self.dpmanage, "dependencies")
            for item in dependencies:
                dp = SubElement(self.dps, 'dependency')
                for child, data in zip(('groupID', 'artifactID', 'version'),
                                       item.split(':')):
                    SubElement(dp, child).text = data

    def xml_string(self):
        return tostring(self.root, encoding='utf-8',
                        xml_declaration=True, pretty_print=True)

