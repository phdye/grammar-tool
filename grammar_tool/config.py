# -*- coding: utf-8 -*-

"""
Grammar Tool configuration
"""

import os
import yaml

from pathlib import Path

from dataclasses import dataclass

from collections import UserDict

from prettyprinter import cpprint as pp

@dataclass
class GrammarSpec:
    name        : str
    description : str
    url         : str
    ext         : str


class GtConfig (UserDict):

    _layers = [ '{base}/config.yaml',
                '{base}/generator/{style}/config.yaml',  # style isn't available yet ?
                '/usr/share/grammar-tool/config.yaml',
                '{home}/config/grammar-tool.yaml',
                '{home}/.config/grammar-tool.yaml',
                '{home}/.grammar-tool.yaml',
              ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base = Path(__file__).parent.resolve(strict=False)
        self.home = os.path.expanduser('~')
        self.model = {}

    def model_fields(self):
        kwargs = {}
        for sym in self.model['FIELDS']:
            try :
                kwargs[sym] = getattr(self, sym)
            except:
                kwargs[sym] = None
        return kwargs

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError("<key> must be a string (str)")
        if key in self.data:
            return self.data[key]
        if key not in self.model:
            raise KeyError(key)
        value = self.model[key]
        if isinstance(value, str):
            value = value.format(**self.model_fields())
            # if key not in self.__getattr__('model')['NOT_A_PATH']:
            if key not in self.model['NOT_A_PATH']:
                value = Path(value)
        if key not in self.model['DYNAMIC']:
            self.data[key] = value
        return value

    def __getattr__(self, key):
        if key in self.data:
            return self.data[key]
        try:
            return self.__getitem__(key)
        except:
            pass
        raise AttributeError

    def __setattribute__(self, key, value, allow_upper=False):
        if not allow_upper and key.isupper():
            raise AttributeError
        self.data[key] = value

    def load(self):

        self.data['layers'] = [ ]

        for layer in self._layers:
            
            config_file = Path(layer.format(home=self.home,
                                            base=self.base,
                                            style=self.style))
            
            try :
                with open(config_file, 'r') as fp:
                    ns = yaml.safe_load(fp)
            except:
                continue

            original_keys = set(self.keys())

            for key, value in ns.items():
                if key in original_keys:
                    raise ValueError(f"Invalid symbol '{key}' in '{config_file}'.  "
                                     f"Must not override original keys {original_keys}")
                key = key.replace('-', '_')
                # if isinstance(value, str):
                #     print(f"- {key:<20}  {value}")
                self.model[key] = value

            self.data['layers'].append(config_file)

        for name, ns in self.GRAMMAR_STYLES.items():
            self.GRAMMAR_STYLES[name] = GrammarSpec(name,
                                                    ns['description'],
                                                    ns['url'],
                                                    ns['extension'])
        return self

