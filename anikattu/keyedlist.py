from collections.abc import MutableMapping

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           super().__repr__())

    
class KeyedList(AttrDict, MutableMapping):
    def __init__(self, *args, **kwargs):
        super().__init__()
        dictionary = dict(*args, **kwargs)
        for key, value in dictionary.items():
            if not isinstance(value, KeyedList):
                try:
                    dictionary[key] = KeyedList(value)
                except (ValueError, TypeError):
                    pass
        self.update(dictionary)

    get = MutableMapping.get
    pop = MutableMapping.pop
    setdefault = MutableMapping.setdefault

    def __getitem__(self, key):
        if '.' in key:
            key, nestedkeys = key.split('.', 1)
            return super().__getitem__(key)[nestedkeys]
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        if '.' in key:
            key, nestedkeys = key.split('.', 1)

            try:
                nestedlist = self[key]
            except KeyError:
                nestedlist = KeyedList()
                super().__setitem__(key, nestedlist)
            else:
                if not isinstance(nestedlist, KeyedList):
                    raise KeyError('target key "%s" is a value, cannot update '
                            'value against another keyed list' % (key,))

            nestedlist[nestedkeys] = value

        else:
            if isinstance(value, KeyedList):
                try:
                    nestedlist = self[key]
                except KeyError:
                    pass
                else:
                    if not isinstance(nestedlist, KeyedList):
                        raise KeyError('target key "%s" is a value, cannot '
                                'update value against another keyed list' %
                                (key,))

            super().__setitem__(key, value)

    def __contains__(self, key):
        if '.' in key:
            key, nestedkeys = key.split('.', 1)

            if super().__contains__(key):
                nestedlist = super().__getitem__(key)
                return nestedlist.__contains__(nestedkeys)
            else:
                return False
        else:
            return super().__contains__(key)

    def __delitem__(self, key):
        if '.' in key:
            key, nestedkeys = key.split('.', 1)

            del super().__getitem__(key)[nestedkeys]

            if not super().__getitem__(key):
                super().__delitem__(key)
        else:
            super().__delitem__(key)

    def update(self, *args, **kwargs):

        if len(args) > 1:
            raise TypeError("update() takes at most 1 positional "
                            "arguments ({} given)".format(len(args)))
        if len(args) >= 1:
            other = args[0]
            if isinstance(other, KeyedList):
                # Merge
                for key, value in other.all_items():
                    self[key] = value
            else:
                MutableMapping.update(self, other)

        for key, value in kwargs.items():
            if isinstance(value, KeyedList):
                try:
                    nestedlist = self[key]
                except KeyError:
                    nestedlist = KeyedList()
                    self[key] = nestedlist
                else:
                    if not isinstance(nestedlist, KeyedList):
                        raise KeyError('target key "%s" is a value, cannot '
                                'update value against another keyed list' %
                                (key,))
                nestedlist.update(value)
            else:
                self[key] = value

    def all_keys(self):
        ret = []

        for key, value in self.items():
            if isinstance(value, KeyedList):
                for subkey in value.all_keys():
                    ret.append(key + '.' + subkey)
            else:
                ret.append(key)

        return ret


    def all_items(self):
        ret = []

        for key, value in self.items():
            if isinstance(value, KeyedList):
                for subkey, subvalue in value.all_items():
                    ret.append((key + '.' + subkey, subvalue))
            else:
                ret.append((key, value))

        return ret

if __name__ == '__main__':

    testlist = KeyedList({

        'model': {
            'module_lstm': {
                'hidden_dim': 200,
                'embed_dim' : 100,
            },

            'module_conv': {
                'padding' : 2,
                'stride'  : 2,
                'height'  : 4,
                'width'   : 3,
            }
        },
        
        'training_config' : {
            'batch_size'    : 20,
            'epochs'        : 200,
            'learning_rate' : 1e-4,
            
        },

        
    })
